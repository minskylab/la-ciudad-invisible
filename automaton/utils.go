package main

import (
	"bytes"
	"image"
	"image/jpeg"
	"io/ioutil"
	"net/http"
	"runtime"

	"github.com/hajimehoshi/ebiten"
	"github.com/pkg/errors"
)

func loadImage(imageURL string) (*ebiten.Image, error) {
	var rawImage image.Image
	if runtime.GOOS == "js" {
		resImg, err := http.Get(imageURL)
		if err != nil {
			return nil, errors.WithStack(err)
		}

		defer resImg.Body.Close()

		rawImage, err = jpeg.Decode(resImg.Body)
		if err != nil {
			return nil, errors.WithStack(err)
		}
	} else {
		data, err := ioutil.ReadFile(imageURL)
		if err != nil {
			return nil, errors.WithStack(err)
		}

		rawImage, err = jpeg.Decode(bytes.NewBuffer(data))
		if err != nil {
			return nil, errors.WithStack(err)
		}
	}

	return ebiten.NewImageFromImage(rawImage, ebiten.FilterDefault)
}
