package scan

import (
	"context"
	"errors"
	"runtime"
	"sync"
	"time"

	"internal/scan/project"
	"internal/scan/system"
)

// Orchestrator is the production-grade scan engine that runs system,
// project and tool detectors and returns a unified ScanResult.
type Orchestrator struct {
	// Detectors is a slice of tool detectors (internal/scan/tools).
	Detectors []Detector

	// WorkerCount limits parallel tool detector goroutines. If 0, computed from CPU.
	WorkerCount int

	// Timeout is the global scan timeout. If zero, a sensible default is used.
	Timeout time.Duration
}

// NewOrchestrator returns a ready-to-run orchestrator. Detectors may be nil.
func NewOrchestrator(detectors []Detector, workerCount int, timeout time.Duration) *Orchestrator {
	if workerCount <= 0 {
		workerCount = runtime.NumCPU() * 2
	}
	if timeout <= 0 {
		timeout = 30 * time.Second
	}
	return &Orchestrator{Detectors: detectors, WorkerCount: workerCount, Timeout: timeout}
}

// Run executes the full scan and returns a populated ScanResult.
// root is the repository root to analyze (can be ".").
func (o *Orchestrator) Run(ctx context.Context, root string) (ScanResult, error) {
	if o == nil {
		return ScanResult{}, errors.New("orchestrator is nil")
	}

	// ensure we have a context with timeout
	if o.Timeout <= 0 {
		o.Timeout = 30 * time.Second
	}
	ctx, cancel := context.WithTimeout(ctx, o.Timeout)
	defer cancel()

	startScan := time.Now()

	// 1) Parallel: start system detection (it is relatively cheap)
	sysCh := make(chan system.SystemInfo, 1)
	sysErrCh := make(chan error, 1)
	go func() {
		defer close(sysCh)
		defer close(sysErrCh)
		// system.DetectSystem accepts context for future-proofing
		res := system.DetectSystem(ctx)
		sysCh <- res
		sysErrCh <- nil
	}()

	// 2) Project detection (IO-bound) — run concurrently but without context cancellation
	projCh := make(chan struct {
		files project.ProjectFilesInfo
		langs []project.LanguageScore
		typeInfo project.ProjectType
		deps project.DependencySummary
		err error
	}, 1)
	go func() {
		var out struct {
			files project.ProjectFilesInfo
			langs []project.LanguageScore
			typeInfo project.ProjectType
			deps project.DependencySummary
			err error
		}

		files, ferr := project.DetectProjectFiles(root)
		if ferr != nil {
			out.err = ferr
			projCh <- out
			return
		}
		out.files = files

		langs, _ := project.DetectLanguages(root)
		out.langs = langs

		typeInfo, _ := project.DetectProjectType(root)
		out.typeInfo = typeInfo

		deps, _ := project.DetectDependencyFiles(root)
		out.deps = deps

		projCh <- out
	}()

	// 3) Tools detectors — run with worker pool
	toolsResults := make(map[string]DetectorResult)
	toolsMu := sync.Mutex{}
	wg := sync.WaitGroup{}

	// detector input channel
	detCh := make(chan Detector)

	// worker function
	worker := func() {
		for det := range detCh {
			select {
			case <-ctx.Done():
				// context cancelled/timeout
				return
			default:
			}
			start := time.Now()
			res := det.Detect(ctx, root)
			res.DurationMs = time.Since(start).Milliseconds()

			toolsMu.Lock()
			toolsResults[det.Name()] = res
			toolsMu.Unlock()
			wg.Done()
		}
	}

	// start workers
	workers := o.WorkerCount
	for i := 0; i < workers; i++ {
		go worker()
	}

	// feed detectors
	for _, d := range o.Detectors {
		wg.Add(1)
		select {
		case <-ctx.Done():
			wg.Done()
			break
		case detCh <- d:
		}
	}

	close(detCh)
	wg.Wait()

	// collect system result
	var sysInfo system.SystemInfo
	if s, ok := <-sysCh; ok {
		sysInfo = s
	} else {
		// fallback empty
		sysInfo = system.SystemInfo{}
	}

	// collect project result
	var projFiles project.ProjectFilesInfo
	var projLangs []project.LanguageScore
	var projType project.ProjectType
	var projDeps project.DependencySummary
	if p := <-projCh; p.err == nil {
		projFiles = p.files
		projLangs = p.langs
		projType = p.typeInfo
		projDeps = p.deps
	} else {
		// leave zero values but capture error in advice
	}

	// Build ScanResult
	sr := ScanResult{
		Success:   ctx.Err() == nil,
		ScannedAt: time.Now().UTC().Format(time.RFC3339),
		System:    map[string]interface{}{},
		Tools:     toolsResults,
		Project:   map[string]interface{}{},
	}

	// attach system info
	sr.System["os"] = map[string]interface{}{
		"name":  sysInfo.OSName,
		"pretty": sysInfo.OSPRETTY,
		"distro": sysInfo.Distro,
		"arch":  sysInfo.Arch,
		"cpu_cores": sysInfo.CPUCores,
		"total_mem_mb": sysInfo.TotalMemMB,
		"containerized": sysInfo.Container,
		"wsl": sysInfo.WSL,
	}

	// attach project info
	projMap := map[string]interface{}{}
	projMap["root"] = projFiles.Root
	projMap["files"] = projFiles.Files
	projMap["detected_at"] = projFiles.DetectedAt
	projMap["languages"] = projLangs
	projMap["project_type"] = projType
	projMap["dependency_summary"] = projDeps
	sr.Project = projMap

	// basic advice: if required tool missing for detected project type
	advice := []map[string]string{}
	// example: if project type is go and go tool missing
	if pt := projType.Type; pt != "" {
		if pt == "go:module" {
			if tr, ok := toolsResults["go"]; !ok || !tr.Present {
				advice = append(advice, map[string]string{"level": "error", "message": "go not installed but go.mod present"})
			}
		}
	}
	sr.Advice = convertAdvice(advice)

	// final timing
	sr.Meta = map[string]interface{}{
		"duration_ms": time.Since(startScan).Milliseconds(),
	}

	return sr, ctx.Err()
}

// convertAdvice converts simple string maps to the expected Advice type.
func convertAdvice(in []map[string]string) []AdviceItem {
	out := []AdviceItem{}
	for _, a := range in {
		out = append(out, AdviceItem{Level: a["level"], Message: a["message"]})
	}
	return out
}


