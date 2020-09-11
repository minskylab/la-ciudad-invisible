import React, { useEffect, useState } from "react";
import {
    ThemeProvider,
    CSSReset,
    ColorModeProvider,
    Grid,
    Box,
    DarkMode,
    PseudoBox,
    Drawer,
    DrawerContent,
    DrawerCloseButton,
    DrawerHeader,
    DrawerBody,
    DrawerOverlay,
    useDisclosure,
    Text,
} from "@chakra-ui/core";
import dynamic from "next/dynamic";
import { SketchProps } from "../components/atoms/sketch";
import Logo from "../components/atoms/logo";

const Sketch = dynamic<SketchProps>(() => import("../components/atoms/sketch") as any, { ssr: false });

const Index = () => {
    const { isOpen, onOpen, onClose } = useDisclosure();
    const btnRef = React.useRef();
    const [sketchSize, setSketchSize] = useState<{ w: number; h: number }>({ w: 600, h: 400 });

    const frameTemplate = (frameSize: number, u: string = "vw"): string => {
        return `${frameSize}vw calc(100${u} - ${2 * frameSize}vw) ${frameSize}vw`;
    };

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
            <CSSReset />
            <ColorModeProvider>
                <DarkMode>
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
                                <Sketch width={sketchSize.w} height={sketchSize.h} />
                            </Box>
                        </Box>
                    </Grid>
                    <Drawer isOpen={isOpen} placement="right" onClose={onClose} finalFocusRef={btnRef}>
                        <DrawerOverlay />
                        <DrawerContent>
                            <DrawerCloseButton color="orange.100" />
                            <DrawerHeader>
                                <Logo scale={3.2} />
                            </DrawerHeader>

                            <DrawerBody>
                                <Text color="white">
                                    El proyecto "La Ciudad Invisible" tiene como finalidad evidenciar los diferentes
                                    eventos de consumo en Cusco llevados a cabo en las redes sociales.
                                </Text>
                            </DrawerBody>
                        </DrawerContent>
                    </Drawer>
                    <PseudoBox
                        ref={btnRef}
                        position="absolute"
                        bottom="1rem"
                        right="1rem"
                        bg={"orange.100"}
                        rounded={3}
                        px={5}
                        py={3}
                        color={"black"}
                        fontWeight="semibold"
                        opacity={0.6}
                        onClick={onOpen}
                        _hover={{
                            cursor: "pointer",
                            opacity: 1.0,
                        }}
                    >
                        ¿Qué es lo que veo?
                    </PseudoBox>
                </DarkMode>
            </ColorModeProvider>
        </ThemeProvider>
    );
};

export default Index;
