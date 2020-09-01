import React, { useRef, useEffect, useState } from "react";
import { ThemeProvider, CSSReset, theme, ColorModeProvider, Grid, Box, useColorMode, DarkMode } from "@chakra-ui/core";
import LCIModal from "../components/molecules/modal";
// import Logo from "../components/atoms/logo";
import dynamic from "next/dynamic";
import { SketchProps } from "../components/atoms/sketch";

const Sketch = dynamic<SketchProps>(() => import("../components/atoms/sketch") as any, { ssr: false });

const Index = () => {
    // const { colorMode, toggleColorMode } = useColorMode();
    const [loading, setLoading] = useState<boolean>(true);

    const frameTemplate = (frameSize: number, u: string = "vw"): string => {
        return `${frameSize}vw calc(100${u} - ${2 * frameSize}vw) ${frameSize}vw`;
    };

    const [sketchSize, setSketchSize] = useState<{ w: number; h: number }>({ w: 600, h: 400 });

    useEffect(() => {
        const newW = window.innerWidth;
        const newH = window.innerHeight;
        setSketchSize({
            w: newW,
            h: newH,
        });
    }, []);
    return (
        <ThemeProvider>
            <ColorModeProvider>
                <DarkMode>
                    <CSSReset />
                    <LCIModal loading={loading} />
                    <Grid templateColumns={frameTemplate(1, "vw")} templateRows={frameTemplate(1, "vh")} bg="black">
                        <Box
                            w="100%"
                            h="100%"
                            bg="black"
                            gridRow="2"
                            gridColumn="2"
                            display="flex"
                            justifyContent="center"
                        >
                            <Box h="100%" display="flex" flexDirection="column" justifyContent="center">
                                <Sketch
                                    width={sketchSize.w}
                                    height={sketchSize.h}
                                    onMounted={() => {
                                        setLoading(false);
                                    }}
                                />
                            </Box>
                        </Box>
                    </Grid>
                </DarkMode>
            </ColorModeProvider>
        </ThemeProvider>
    );
};

export default Index;
