package main

import (
	"math"
	"math/rand"
)

// HighLife represents the new neighbor to born
type HighLife uint8

// NoHighLife isn't highlife
const NoHighLife HighLife = 0

// HighLife8 borns at 8
const HighLife8 HighLife = 8

// HighLife7 borns at 7
const HighLife7 HighLife = 7

// HighLife6 borns at 6
const HighLife6 HighLife = 6

// HighLife5 borns at 5
const HighLife5 HighLife = 5

// HighLife4 borns at 4
const HighLife4 HighLife = 4

// HighLife456 borns at 4
const HighLife456 HighLife = 1

// GOL ...
type GOL struct {
	area     []uint8
	width    int
	height   int
	highLife HighLife
}

// NewGOL ...
func NewGOL(width, height int, highLife HighLife) *GOL {
	return &GOL{
		area:     make([]uint8, width*height),
		width:    width,
		height:   height,
		highLife: highLife,
	}
}

func (g *GOL) randomFill(density float32) {
	for y := 0; y < g.height; y++ {
		for x := 0; x < g.width; x++ {
			if rand.Float32() < density {
				g.area[y*g.width+x] = 0x01
			}
		}
	}
}

// Update ...
func (g *GOL) Update() {
	width := g.width
	height := g.height
	next := make([]uint8, width*height)

	neighbours := g.neighbourArea() // make([]uint8, width*height)
	for i := 0; i < g.height*g.width; i++ {
		// if neighbours[i] == 0 && g.area[i] == 0 {
		// 	continue
		// }

		c1 := (g.area[i] > 0 && neighbours[i] == 2)
		c1 = neighbours[i] == 3 || c1

		if g.highLife == HighLife456 {
			c1 = neighbours[i] == uint8(4) || neighbours[i] == uint8(5) || neighbours[i] == uint8(6) || c1
		} else if g.highLife > 0 {
			c1 = neighbours[i] == uint8(g.highLife) || c1
		}

		if c1 {
			next[i] = 1
		}
	}

	g.area = next
}

// DrawRandomStains ...
func (g *GOL) DrawRandomStains(numbers int, minDia, maxDia float64) {
	for i := 0; i < numbers; i++ {
		x := rand.Intn(g.width)
		y := rand.Intn(g.height)
		r := int(rand.Float64()*(maxDia-minDia) + minDia)
		g.DrawStain(x, y, r)
	}
}

// RandomFill ...
func (g *GOL) RandomFill(density float32) {
	g.randomFill(density)
}

// DrawStain ...
func (g *GOL) DrawStain(x, y, d int) {
	for i := x - (d / 2); i < x+(d/2); i++ {
		for j := y - (d / 2); j < y+(d/2); j++ {
			if i <= 0 || j <= 0 || i > g.width-1 || j > g.height-1 {
				continue
			}

			dist := math.Sqrt(float64((i-x)*(i-x) + (j-y)*(j-y)))
			if dist > float64(d/2) {
				continue
			}

			if rand.Float32() < 0.2 {
				g.area[j*g.width+i] = 0x01
			}
		}
	}

}

// Draw paints current game state.
func (g *GOL) Draw(pix []byte) {
	setPixel := func(index int, color [4]byte) {
		for j := 0; j < 4; j++ {
			if 4*index+j < len(pix) {
				pix[4*index+j] = color[j]
			}
		}
	}

	for i, v := range g.area {
		color := byte(0x00)
		if v > 0x00 {
			color = 0xff
		}
		setPixel(i, [4]byte{color, color, color, color})
	}

}

func (g *GOL) neighbourArea() []uint8 {
	neighboursArea := make([]uint8, g.width*g.height)
	for y := 0; y < g.height; y++ {
		for x := 0; x < g.width; x++ {
			c := uint8(0)
			for j := -1; j <= 1; j++ {
				for i := -1; i <= 1; i++ {
					if i == 0 && j == 0 {
						continue
					}

					x2 := x + i
					y2 := y + j

					if x2 < 0 || y2 < 0 || g.width <= x2 || g.height <= y2 {
						continue
					}
					if g.area[y2*g.width+x2] > 0 {
						c++
					}
				}
			}
			neighboursArea[y*g.width+x] += c
		}
	}

	return neighboursArea
}

/*
fX, fY := x, y

if fX == 0 {
	fX = 1
}

if fY == 0 {
	fY = 1
}

if fX == g.width-1 {
	fX = g.width - 2
}

if fY == g.height-1 {
	fY = g.height - 2
}

c := g.area[(fY+-1)*g.width+(fX+-1)] +
	 g.area[(fY+-1)*g.width+(fX+0)] +
	 g.area[(fY+-1)*g.width+(fX+1)] +
	 g.area[(fY+0)*g.width+(fX+-1)] +
	 g.area[(fY+0)*g.width+(fX+1)] +
	 g.area[(fY+1)*g.width+(fX+-1)] +
	 g.area[(fY+1)*g.width+(fX+0)] +
	 g.area[(fY+1)*g.width+(fX+1)]

*/
