import { withTheme } from 'emotion-theming'
import {
  Link as ChakraLink,
  Text,
  Heading,
  Stack,
  Input,
  Button,
  Box,
} from '@chakra-ui/core'

import { Container } from '../components/Container'
import { Main } from '../components/Main'
import { DarkModeSwitch } from '../components/DarkModeSwitch'
import { CTA } from '../components/CTA'
import { Footer } from '../components/Footer'
import { useState } from 'react'

const Index = () => {
  
  const [sentence, setSentence] = useState("")
  const [isLoading, setLoading] = useState(false)
  const [amr, setAMR] = useState(null)

  const onSentenceChange = (event) => {
    setSentence(event.target.value);
  }

  const onParseButtonClick = async (event) => {
    const cleanedSentence = sentence.split(' ').join("%20")
    setLoading(true)
    fetch(`http://localhost:5000/predict?sentence=${cleanedSentence}`)
      .then(response => response.json())
      .then(data => data.img)
      .then(img => setAMR(`data:image/png;base64,${img}`))
      .then(setLoading(false))
  }
  
  return (
  <Container>
    <Main>
      <Heading fontSize="3vw">
        AMR Parser for Bahasa Indonesia
    </Heading>
      <Text fontSize="1vw">Based on Pembangkitan Graf Abstract Meaning Representation Berbahasa Indonesia</Text>

      <Stack my="5vh" align="center" spacing={5} minW="30vw">
        <Heading fontSize="2vw">Enter a sentence: </Heading>
        <Input placeholder="Example: Pak Dodi makan kue di Bandung di pagi hari" size="md" onChange={onSentenceChange}/>
        <Button alignSelf="end" size="md" onClick={onParseButtonClick} isLoading={isLoading}>Parse</Button>   
      </Stack>

    {!isLoading && amr && (
      <>
      <Heading fontSize="1.5vw">Result: </Heading>
      <Box p={5} borderWidth="1px" borderRadius="5pt" mt="2vh">
        <img src={amr}></img>
      </Box>
      </>
    )}

  </Main>


    <DarkModeSwitch />
    <Footer>
      <Text>Made By Adylan Roaffa Ilmy</Text>
    </Footer>
  </Container>
)}

export default withTheme(Index)