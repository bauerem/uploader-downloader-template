import  { Routes, Route, Link } from "react-router-dom";
import { ChakraProvider } from '@chakra-ui/react';
import { Box, Flex } from '@chakra-ui/react'

import { Home } from "./pages/Home";
import { Time } from "./pages/Time";
import { NotFound } from "./pages/NotFound";

function App() {
  return (
    <ChakraProvider>
      <div>

        <Flex justifyContent="right" height="20vh">
          <Box margin="2em">
            <Link to="/">Home</Link>
          </Box>
          <Box margin="2em">
            <Link to="/time">Time</Link>
          </Box>
        </Flex>

        <Flex alignItems='center' justifyContent='center' height='60vh'>
          <Routes>
              <Route path='*' element={<NotFound />} />
              <Route path='/' element={<Home />} />
              <Route path='/time' element={<Time />} />
          </Routes>
        </Flex>

      </div>
    </ChakraProvider>
  );
}

export default App;
