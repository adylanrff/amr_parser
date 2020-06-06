import { Flex, Heading } from '@chakra-ui/core'

export const Hero = ({ title }) => (
  <Flex justifyContent="center" alignItems="center" height="100vh">
    <Heading fontSize="3vw">{title}</Heading>
  </Flex>
)

Hero.defaultProps = {
  title: 'AMR Parser for Bahasa Indonesia',
}
