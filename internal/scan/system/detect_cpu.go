package system


import "runtime"


// DetectCPU returns the number of CPU cores.
func DetectCPU() int {
return runtime.NumCPU()
}
