// frontend/src/App.jsx
import { CssBaseline, Container, Box } from '@mui/material';
import FileUploadDemo from './components/FileUploadDemo';

function App() {
  return (
    <>
      {/* CssBaseline kickstarts an elegant, consistent, and simple baseline to build upon. */}
      <CssBaseline />
      <Container maxWidth="md">
        <Box sx={{ my: 4 }}>
          <FileUploadDemo />
        </Box>
      </Container>
    </>
  );
}

export default App;