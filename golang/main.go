package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

func main() {
	c := make(chan int)
	var value int
	go func() {
		fmt.Println("Entrou")
		fmt.Println("Recebeu 1")
		c <- 1
		fmt.Println("Recebeu 2")
		c <- 1
	}()
	fmt.Println("Print canal")
	fmt.Println(c)
	fmt.Println("Print 1")
	fmt.Println(<-c)
	value = <-c
	fmt.Println("Print 2")
	fmt.Println(value)
	// startTime := time.Now()
	// defer getTimeElapsed(startTime)
	// // readFileSequential("..\\temp_files\\exemplo.txt")
	// // readFileRoutine("..\\temp_files\\exemplo.txt")
	// var downloadableContentUrlPath, filePath, fileType string
	// var totalPartitions int
	// var useConcurrency bool
	// downloadableContentUrlPath = "https://www.sample-videos.com/csv/Sample-Spreadsheet-500000-rows.csv"
	// useConcurrency = false
	// if useConcurrency {
	// 	fileType = "concurrent"
	// } else {
	// 	fileType = "sequence"
	// }
	// filePath = fmt.Sprintf("..\\temp_files\\golang\\free_dummy_data_%v.csv", fileType)
	// totalPartitions = 28 // care about website server limit
	// RunDownload(downloadableContentUrlPath, filePath, totalPartitions, useConcurrency)
}

func getTimeElapsed(startTime time.Time) float64 {
	finishTime := time.Since(startTime).Seconds()
	fmt.Printf("Start Time   = %v:%v:%v\n", startTime.Hour(), startTime.Minute(), startTime.Second())
	fmt.Println("Finish Time  =", finishTime)
	return finishTime
}

func readString(str string, match string) string {
	if strings.Contains(str, match) {
		return str
	}
	return ""
}

func readFileSequential(fileName string) {
	file, err := os.Open(fileName)
	if err != nil {
		panic(err)
	}
	scan := bufio.NewScanner(file)
	var lines []string

	for scan.Scan() {
		line := scan.Text()
		result := readString(line, "junior")
		if result != "" {
			// fmt.Println(result)
			lines = append(lines, line)
		}
	}
	defer fmt.Println(lines)
}

func readFileRoutine(fileName string) {
	var wg sync.WaitGroup // Added a wait group to keep track of Goroutines
	file, err := os.Open(fileName)
	if err != nil {
		panic(err)
	}
	scan := bufio.NewScanner(file)
	var lines []string
	for scan.Scan() {
		wg.Add(1)   // Add 1 on WaitGroup for each Goroutine ("for" loop runs count)
		go func() { // Declaring anonymous goroutine
			line := scan.Text()
			result := readString(line, "junior")
			if result != "" {
				// fmt.Println(result)
				lines = append(lines, line)
			}
			wg.Done() // Telling WaitGroup that one Goroutine ended
		}() // No need to pass parameters if all the work are in the loop
	}
	wg.Wait() // To wait all Goroutines to finish
	defer fmt.Println(lines)
}

// Go Downloader
type Download struct {
	Url             string
	FilePath        string
	TotalPartitions int
}

func RunDownload(url string, filePath string, totalPartitions int, useConcurrency bool) {
	os.Remove(filePath) // Remove file if it already exists
	download := Download{
		// Provide the URL to access and download,
		Url: url,
		// Provide the file path with extension, example: example.csv
		FilePath: filePath,
		// Number of partitions/connections to make to the server
		TotalPartitions: totalPartitions,
	}
	err := download.Do(useConcurrency)
	if err != nil {
		log.Printf("An error occured while downloading the file: %s\n", err)
	}
}

// Get a new http request
func (download Download) getNewRequest(method string) (*http.Request, error) {
	request, err := http.NewRequest(method, download.Url, nil)
	if err != nil {
		return nil, err
	}
	request.Header.Set("User-Agent", "Go Downloader")
	return request, nil
}

// Start the download
func (download Download) Do(useConcurrency bool) error {
	fmt.Println("Checking URL")
	request, err := download.getNewRequest("HEAD")
	if err != nil {
		return err
	}
	response, err := http.DefaultClient.Do(request)
	if err != nil {
		return err
	}
	fmt.Printf("Response StatusCode: %v\n", response.StatusCode)

	if response.StatusCode > 299 {
		return fmt.Errorf("can't process, response is %v", response.StatusCode)
	}

	size, err := strconv.Atoi(response.Header.Get("Content-Length"))
	if err != nil {
		return err
	}
	fmt.Printf("Size is %v bytes\n", size)

	var partitions = make([][2]int, download.TotalPartitions)
	eachSize := size / download.TotalPartitions
	fmt.Printf("Each size is %v bytes\n", eachSize)

	for index := range partitions {
		if index == 0 {
			partitions[index][0] = 0 // starting byte of first partition
		} else {
			partitions[index][0] = partitions[index-1][1] + 1 // starting byte of other partitions
		}
		if index < download.TotalPartitions-1 {
			partitions[index][1] = partitions[index][0] + eachSize // ending byte of other partitions
		} else {
			partitions[index][1] = size - 1 // ending byte of last partition
		}
	}
	fmt.Println("Partition(s):\n", partitions)
	switch useConcurrency {
	case false: // Download each partition sequentially
		for index, partition := range partitions {
			err = download.downloadPartition(index, partition)
			if err != nil {
				panic(err)
			}
		}
	case true: // Download each partition concurrently
		var wg sync.WaitGroup
		for index, partition := range partitions {
			wg.Add(1)
			go func(index int, partition [2]int) {
				defer wg.Done()
				err = download.downloadPartition(index, partition)
				if err != nil {
					panic(err)
				}
			}(index, partition)
		}
		wg.Wait()
	}
	return download.mergeFiles(partitions)
}

// Download a single partition and save content to a temporary file
func (download Download) downloadPartition(index int, content [2]int) error {
	request, err := download.getNewRequest("GET")
	if err != nil {
		return err
	}
	request.Header.Set("Range", fmt.Sprintf("bytes=%v-%v", content[0], content[1]))
	response, err := http.DefaultClient.Do(request)
	if err != nil {
		return err
	}
	if response.StatusCode > 299 {
		return fmt.Errorf("can't process, response is %v", response.StatusCode)
	}
	fmt.Printf("Downloaded %v bytes for partition %v\n", response.Header.Get("Content-Length"), index+1)
	bytes, err := ioutil.ReadAll(response.Body)
	if err != nil {
		return err
	}
	err = ioutil.WriteFile(fmt.Sprintf("partition-%v.tmp", index), bytes, os.ModePerm)
	if err != nil {
		return err
	}
	return nil
}

// Merge temporary files pieces into a single file and delete temporary files
func (download Download) mergeFiles(partitions [][2]int) error {
	file, err := os.OpenFile(download.FilePath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, os.ModePerm)
	if err != nil {
		return err
	}
	defer file.Close()
	var totalBytesMerged int
	for index := range partitions {
		temporaryFileName := fmt.Sprintf("partition-%v.tmp", index)
		bytes, err := ioutil.ReadFile(temporaryFileName)
		if err != nil {
			return err
		}
		numberOfBytes, err := file.Write(bytes)
		if err != nil {
			return err
		}
		err = os.Remove(temporaryFileName)
		if err != nil {
			return err
		}
		totalBytesMerged += numberOfBytes
	}
	fmt.Printf("Total of bytes merged: %v\n", totalBytesMerged)
	return nil
}
