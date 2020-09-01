import p5 from "p5";
import VirtualEffect from "./virtualeffect";
import Automaton from "./automaton";

const mainSketchFactory = (width?: number, height?: number) => {
    let pImages: p5.Image[];
    let realities: VirtualEffect[];

    const cellSize: number = 4; // 18
    const images = ["/im4.jpg", "/im3.jpg"];

    return (p: p5): void => {
        p.preload = () => {
            pImages = images.map((imgSrc): p5.Image => p.loadImage(imgSrc));
        };

        p.setup = () => {
            console.log(width, height);
            p.createCanvas(width || 500, height || 500);
            p.colorMode(p.RGB, 255);
            p.noStroke();

            realities = pImages.map((img, index) => {
                const automaton = new Automaton(
                    p,
                    cellSize,
                    {
                        0: p.color(255, 0), // 0 alpha
                        1: p.color(255, 255), // 255 alpha
                    }
                    // { 6: index === 0 ? 0 : 1 },
                    // { 6: index === 0 ? 0 : 1 }
                );
                return new VirtualEffect(p, automaton, img, p.MULTIPLY);
            });
        };

        const showFps = () => {
            let fps = p.frameRate();
            p.fill(255);
            p.stroke(0);
            p.text("FPS: " + fps.toFixed(2), 10, height - 10);
        };

        p.draw = () => {
            p.background("#000");
            realities.map((r) => r.draw(p));
            realities.map((r) => r.update());
            showFps();
        };
    };
};

export default mainSketchFactory;
