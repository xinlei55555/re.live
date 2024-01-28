import React, { createContext, useEffect } from "react";
import Ghost from "./Components/AnimationObjects/Ghost";
import "./App.css";
export const PosnContext = createContext({}); // 0 is just a placeholder

const App: React.FC = () => {
  const [posn, setPosn] = React.useState({ x: -100, y: 0 }); // [x, y, z]
  useEffect(() => {
    const mover = setInterval(() => {
      // Using the previous state to update the position
      setPosn((prevPosn) => ({ x: 100, y: 200 }));
    }, 1000);

    // Clear the interval when the component unmounts
    return () => clearInterval(mover);
  }, []); // Empty dependency array ensures the effect runs only once after the initial render

  // Log the updated position in a separate effect to see the correct value
  useEffect(() => {
    console.log(posn);
  }, [posn]); // Effect will run whenever posn changes
  return (
    <div className="App">
      <PosnContext.Provider value={[posn, setPosn]}>
        <Ghost />
      </PosnContext.Provider>
    </div>
  );
};

export default App;
