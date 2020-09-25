package main

import (
	"math/rand"
	"syscall/js"
	"time"
)

const (
	screenHeight = 320 // 420, 520
	screenWidth  = screenHeight * 16 / 9
)

func init() {
	rand.Seed(time.Now().UnixNano())
}

func (ec *EmergentCity) insertNewEvent(this js.Value, inputs []js.Value) interface{} {
	if len(inputs) < 3 {
		return nil
	}

	// fmt.Println(inputs)

	image := inputs[0].String()
	duration := inputs[1].String()
	relevance := inputs[2].Float()

	// fmt.Println(image, duration, relevance)

	go ec.InsertNewEvent(image, duration, float32(relevance))

	return nil
}

func main() {
	done := make(chan struct{})
	ec := NewEmergentCity()

	js.Global().Set("insertNewEvent", js.FuncOf(ec.insertNewEvent))

	ec.Run()
	<-done
}
