package main

import (
	"fmt"
	"sync"
	"time"

	"github.com/hajimehoshi/ebiten"
)

// EmergentCity ...
type EmergentCity struct {
	mu   *sync.Mutex
	city *InvisibleCity
}

// NewEmergentCity ...
func NewEmergentCity() *EmergentCity {
	N := 2
	categories := make([]*Category, N)

	for i := 0; i < N; i++ {
		categories[i] = NewCategory(screenWidth, screenHeight, NoHighLife)
	}

	inv := &InvisibleCity{
		categories: categories,
	}

	ec := &EmergentCity{city: inv, mu: &sync.Mutex{}}

	return ec
}

// Run ...
func (ec *EmergentCity) Run() {
	ebiten.SetRunnableOnUnfocused(true)
	ebiten.SetMaxTPS(20)
	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetFullscreen(true)
	ebiten.SetWindowTitle("Emergence Life")
	ebiten.RunGame(ec.city)
}

func (ec *EmergentCity) insertationRoutine(index int, duration time.Duration) {
	ec.mu.Lock()

	start := time.Now()
	final := start.Add(duration / 2)

	ec.city.categories[index].SetHighLifeMode(HighLife456)
	// ec.city.categories[index].SetHighLifeMode(HighLife4)

	for time.Now().Before(final) {
		ec.city.categories[index].gol.RandomFill(0.03)
		time.Sleep(55 * time.Millisecond)
	}

	// ec.city.categories[index].SetHighLifeMode(HighLife5)
	// time.Sleep(duration / 2)

	// ec.city.categories[index].SetHighLifeMode(HighLife6)
	time.Sleep(duration / 2 / 4)
	// ec.city.categories[index].SetHighLifeMode(HighLife7)
	time.Sleep(duration / 2 / 4)
	ec.city.categories[index].SetHighLifeMode(HighLife4)
	time.Sleep(duration / 2 / 4)
	ec.city.categories[index].SetHighLifeMode(HighLife6)
	time.Sleep(duration / 2 / 4)
	ec.city.categories[index].SetHighLifeMode(HighLife7)
	time.Sleep(duration / 2 / 4)
	ec.city.categories[index].SetHighLifeMode(NoHighLife)

	ec.mu.Unlock()
}

func (ec *EmergentCity) insertEvent(i int, imageURL string, duration time.Duration, relevance float32) {
	ec.mu.Lock()
	ec.city.categories[i].SetImage(imageURL)
	ec.city.categories[i].SetRelevance(relevance)
	go ec.insertationRoutine(i, duration)
	ec.mu.Unlock()
}

func (ec *EmergentCity) swapCategories(from, to int) {
	ec.mu.Lock()

	backupImageURL := ec.city.categories[to].imageURL
	backupRelevance := ec.city.categories[to].relevance

	ec.city.categories[to].image = nil
	ec.city.categories[to].SetImage(ec.city.categories[from].imageURL)
	ec.city.categories[to].SetRelevance(ec.city.categories[from].relevance)

	ec.city.categories[from].image = nil
	ec.city.categories[from].SetImage(backupImageURL)
	ec.city.categories[from].SetRelevance(backupRelevance)

	ec.mu.Unlock()
}

func (ec *EmergentCity) removeImage(index int) {
	ec.mu.Lock()
	ec.city.categories[index].image = nil
	ec.mu.Unlock()
}

func (ec *EmergentCity) categoryImageIsNil(index int) bool {
	ec.mu.Lock()
	res := ec.city.categories[index].image == nil
	ec.mu.Unlock()
	return res
}

// InsertNewEvent ...
func (ec *EmergentCity) InsertNewEvent(imageURL string, duration string, relevance float32) {
	dur, _ := time.ParseDuration(duration)

	fmt.Printf(
		"Starting insertion of \"%s\", rel=%.3f, (%v, %v)\n",
		imageURL,
		relevance,
		ec.categoryImageIsNil(0),
		ec.categoryImageIsNil(1),
	)

	if ec.categoryImageIsNil(0) && ec.categoryImageIsNil(1) {
		ec.insertEvent(1, imageURL, dur, relevance)
		return
	}

	if ec.categoryImageIsNil(0) {
		if ec.city.categories[1].relevance > relevance {
			ec.insertEvent(0, imageURL, dur, relevance)
		} else {
			ec.swapCategories(1, 0)
			ec.insertEvent(1, imageURL, dur, relevance)
		}
		return
	}

	if ec.categoryImageIsNil(1) {
		if ec.city.categories[0].relevance > relevance {
			ec.swapCategories(0, 1)
			ec.insertEvent(0, imageURL, dur, relevance)
		} else {
			ec.insertEvent(1, imageURL, dur, relevance)
		}
		return
	}

	if ec.city.categories[0].lastUpdate.After(ec.city.categories[1].lastUpdate) {
		ec.removeImage(0)
	} else {
		ec.removeImage(1)
	}

	ec.InsertNewEvent(imageURL, duration, relevance)
}
