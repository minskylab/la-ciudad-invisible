import p5 from "p5";
import Automaton from "./automaton";

class VirtualEffect {
    automaton: Automaton;
    image: p5.Image;
    blendMode: p5.BLEND_MODE;

    constructor(p: p5, automaton: Automaton, image: p5.Image, blendMode?: p5.BLEND_MODE) {
        this.automaton = automaton;
        this.image = image;
        this.blendMode = blendMode || p.DARKEST;
    }

    draw(p: p5) {
        const board = p.createImage(p.width, p.height); //.getBlendedState(this.image);
        board.copy(this.image, 0, 0, this.image.width, this.image.height, 0, 0, board.width, board.height);
        board.mask(this.automaton.getImageState(p));
        p.image(board, 0, 0);
        // p.ellipse(p.mouseX, p.mouseY, 10, 10);
    }

    update() {
        this.automaton.updateState(); // 4 fps +
    }
}

export default VirtualEffect;
