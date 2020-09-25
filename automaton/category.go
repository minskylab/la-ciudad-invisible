package main

import (
	"time"

	"github.com/hajimehoshi/ebiten"
	"github.com/pkg/errors"
)

// Category is a necessary wrapper
type Category struct {
	board      *ebiten.Image
	image      *ebiten.Image
	pix        []byte
	gol        *GOL
	relevance  float32
	lastUpdate time.Time
	imageURL   string
}

// NewCategory ...
func NewCategory(w, h int, highLife HighLife) *Category {
	g := NewGOL(w, h, highLife)

	board, _ := ebiten.NewImage(w, h, ebiten.FilterDefault)

	return &Category{
		gol:        g,
		board:      board,
		pix:        make([]byte, 4*g.width*g.height),
		lastUpdate: time.Now(),
	}
}

// Draw ...
func (c *Category) Draw(screen *ebiten.Image) {
	c.gol.Draw(c.pix)
	c.gol.Update()

	if c.image != nil {
		w, h := c.image.Size()
		c.board.ReplacePixels(c.pix)

		imgOp := &ebiten.DrawImageOptions{}
		imgOp.CompositeMode = ebiten.CompositeModeSourceIn
		imgOp.ColorM.ChangeHSV(0.0, 1.4, 1.0)
		imgOp.GeoM.Scale(screenWidth/float64(w), screenHeight/float64(h))

		c.board.DrawImage(c.image, imgOp)
	}

	op := &ebiten.DrawImageOptions{}

	screen.DrawImage(c.board, op)
}

// SetImage ...
func (c *Category) SetImage(imageURL string) error {
	img, err := loadImage(imageURL)
	if err != nil {
		return errors.WithStack(err)
	}

	c.image = img
	c.imageURL = imageURL
	c.lastUpdate = time.Now()
	return nil
}

// SetRelevance ...
func (c *Category) SetRelevance(relevance float32) {
	c.relevance = relevance
}

// SetHighLifeMode ...
func (c *Category) SetHighLifeMode(mode HighLife) {
	c.gol.highLife = mode
}
