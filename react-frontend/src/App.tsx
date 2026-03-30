import { BrowserRouter, Routes, Route } from 'react-router-dom';
import FigmaApp from './figma-ui/App';
import { LandingPage } from './figma-ui/components/LandingPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/app" element={<FigmaApp />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
