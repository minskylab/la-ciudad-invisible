import React, { useEffect, useState, useRef } from "react";
import {
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton,
    Button,
    useDisclosure,
    Progress,
    Box,
} from "@chakra-ui/core";
import Logo from "../atoms/logo";

interface LCIModalProps {
    loading?: boolean;
}

const LCIModal: React.FC<LCIModalProps> = ({ loading = false }) => {
    const { isOpen, onOpen, onClose } = useDisclosure();
    const [progress, setProgress] = useState<number>(0);
    const [barVisibility, setBarVisibility] = useState<boolean>(loading);

    useEffect(onOpen, []);
    useEffect(() => {
        let i: NodeJS.Timeout;
        if (loading) {
            i = setInterval(() => {
                setProgress((prevProgress) => prevProgress + 1);
            }, 60);
        } else {
            setProgress(100);
            i && clearInterval(i);
            setTimeout(() => setBarVisibility(false), 500);
        }

        return () => {
            i && clearInterval(i);
        };
    }, [loading]);

    return (
        <>
            <Modal isOpen={isOpen} onClose={onClose}>
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>
                        <Logo scale={3.2} />
                    </ModalHeader>
                    <ModalCloseButton color="orange.100" />
                    <ModalBody>
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. A commodi illo laudantium optio
                        explicabo minus ullam accusantium dolore eum enim dolor error tempora, laboriosam possimus
                        eveniet repellat id repellendus vitae?
                        <Box mt="5">
                            <Progress
                                hasStripe
                                isAnimated
                                color="orange"
                                value={progress}
                                opacity={barVisibility ? 1 : 0}
                            />
                        </Box>
                    </ModalBody>
                    <ModalFooter>
                        {/* <Button variantColor="blue" mr={3} onClick={onClose}>
                            Cerrar
                        </Button> */}

                        <Button onClick={onClose} variantColor="orange">
                            Ok
                        </Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </>
    );
};

export default LCIModal;
