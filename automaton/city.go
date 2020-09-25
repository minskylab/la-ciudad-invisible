package main

import (
	"fmt"

	"github.com/hajimehoshi/ebiten"
	"github.com/hajimehoshi/ebiten/ebitenutil"
)

// InvisibleCity ...
type InvisibleCity struct {
	debug      bool
	categories []*Category
}

// Update ...
func (g *InvisibleCity) Update(screen *ebiten.Image) error {
	for _, cat := range g.categories {
		cat.Draw(screen)
	}

	if g.debug {
		ebitenutil.DebugPrint(screen, fmt.Sprintf("TPS: %0.2f", ebiten.CurrentTPS()))
	}

	return nil
}

// Layout returns the geometry of the ebiten screen
func (g *InvisibleCity) Layout(outsideWidth, outsideHeight int) (int, int) {
	return screenWidth, screenHeight
}
