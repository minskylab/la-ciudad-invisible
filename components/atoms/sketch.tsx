import React, { useEffect, useRef } from "react";
import mainSketchFactory from "./ca";
import { Box } from "@chakra-ui/core";
import p5 from "p5";

export interface SketchProps {
    width?: number;
    height?: number;
    onMounted?: () => void;
}

const Sketch: React.FC<SketchProps> = ({ width = 100, height = 100, onMounted }: SketchProps) => {
    const artboardRef = useRef<HTMLElement>();

    useEffect(() => {
        const mainSketch = mainSketchFactory(width, height);
        if (artboardRef.current && artboardRef.current.hasChildNodes()) {
            if (artboardRef.current.childNodes.length > 0) {
                artboardRef.current.removeChild(artboardRef.current.childNodes[0]);
            }
        }

        new p5(mainSketch, artboardRef.current);

        onMounted && onMounted();
    }, []);
    return <Box ref={artboardRef} />;
};

export default Sketch;
