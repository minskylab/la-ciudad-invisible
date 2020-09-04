import React, { useRef, useEffect, useState } from "react";
import {
    ThemeProvider,
    CSSReset,
    theme,
    ColorModeProvider,
    Grid,
    Box,
    useColorMode,
    DarkMode,
    PseudoBox,
    Drawer,
    DrawerContent,
    DrawerCloseButton,
    DrawerHeader,
    DrawerBody,
    Input,
    DrawerFooter,
    Button,
    DrawerOverlay,
    useDisclosure,
} from "@chakra-ui/core";
import LCIModal from "../components/molecules/modal";
// import Logo from "../components/atoms/logo";
import dynamic from "next/dynamic";
import { SketchProps } from "../components/atoms/sketch";
import Logo from "../components/atoms/logo";

const Sketch = dynamic<SketchProps>(() => import("../components/atoms/sketch") as any, { ssr: false });

const Index = () => {
    // const { colorMode, toggleColorMode } = useColorMode();
    // const [loading, setLoading] = useState<boolean>(true);
    const { isOpen, onOpen, onClose } = useDisclosure();
    const btnRef = React.useRef();

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
                <CSSReset />
                {/* <LCIModal loading={loading} /> */}
                <Grid templateColumns={frameTemplate(1, "vw")} templateRows={frameTemplate(1, "vh")} bg="black">
                    <Box w="100%" h="100%" bg="black" gridRow="2" gridColumn="2" display="flex" justifyContent="center">
                        <Box h="100%" display="flex" flexDirection="column" justifyContent="center">
                            <Sketch
                                width={sketchSize.w}
                                height={sketchSize.h}
                                // onMounted={() => {
                                //     setLoading(false);
                                // }}
                            />
                        </Box>
                    </Box>
                </Grid>
                <Drawer isOpen={isOpen} placement="right" onClose={onClose} finalFocusRef={btnRef}>
                    <DrawerOverlay />
                    <DrawerContent>
                        <DrawerCloseButton />
                        <DrawerHeader>
                            <Logo scale={3.2} colorA={"#FFB55B"} colorB={"#000000"} />
                        </DrawerHeader>

                        <DrawerBody>
                            El proyecto "La Ciudad Invisible" tiene como finalidad evidenciar los diferentes eventos de
                            consumo en Cusco llevados a cabo en las redes sociales.
                        </DrawerBody>

                        <DrawerFooter>
                            {/* <Button variant="outline" mr={3} onClick={onClose}>
                                Cancel
                            </Button>
                            <Button color="blue">Save</Button> */}
                        </DrawerFooter>
                    </DrawerContent>
                </Drawer>
                <PseudoBox
                    ref={btnRef}
                    position="absolute"
                    bottom="1rem"
                    right="1rem"
                    bg={"white"}
                    rounded={3}
                    px={5}
                    py={3}
                    color={"black"}
                    fontWeight="semibold"
                    opacity={0.52}
                    onClick={onOpen}
                    _hover={{
                        cursor: "pointer",
                        opacity: 1.0,
                    }}
                >
                    ¿Qué es lo que veo?
                </PseudoBox>
            </ColorModeProvider>
        </ThemeProvider>
    );
};

export default Index;
