import React, { createContext, useEffect, useState } from "react";
import Ghost from "./Components/AnimationObjects/Ghost";
import { ChatInput } from "./Components/ChatInput";
import { CarouselContainer } from "./Components/CarouselContainer";
import "./App.css";
import disco from "./disco.gif";
import img from "./img.png"; // Tell webpack this JS file uses this image
import logo from "./logo.png";
import { FinalPage } from "./Components/FinalPage";
export const PosnContext = createContext({}); // 0 is just a placeholder
export const keyboardShownContext = createContext({}); // 0 is just a placeholder
import Beat_It from "./Beat_It.mp3";

const App = () => {
  const [posn, setPosn] = useState({
    ghostX: 60,
    ghostY: 100,
    textInitial: 0,
    textFinal: 0,
    musicCardInitial: 0,
    musicCardFinal: 1,
    danceCardInitial: 0,
    danceCardFinal: 1,
  }); // [x, y, z]
  const [music, setMusic] = useState(null);
  const [dance, setDance] = useState(null);
  const [keyboardShown, setKeyboardShown] = useState({ status: false });
  const [textContent, setTextContent] = useState("");
  const [showMusicCarousel, setShowMusicCarousel] = useState(false);
  const [showDanceCarousel, setshowDanceCarousel] = useState(false);
  const [carouselContent, setCarouselContent] = useState([]);
  const [isFinalStage, setIsFinalStage] = useState(false);
  const [emotion, setEmotion] = useState(null);
  useEffect(() => {
    var audio = new Audio(Beat_It);
    audio.play();
    // First animation
    const mover = setTimeout(() => {
      // Using the previous state to update the position
      setTimeout(() => {
        // Using the previous state to update the position
        setPosn((prevPosn) => ({
          ghostX: 100,
          ghostY: 200,
          textInitial: 0,
          textFinal: 1,
        }));
        setTextContent("Hi! I am DiSco! How are you feeling today?");
        setKeyboardShown({ status: true });
      }, 1000);
      setPosn((prevPosn) => ({ ...prevPosn, ghostX: 100, ghostY: 200 }));
    }, 1000);

    // Clear the interval when the component unmounts
    return () => clearTimeout(mover);
  }, []); // Empty dependency array ensures the effect runs only once after the initial render

  const finalCall = () => {
    setTimeout(() => {
      setIsFinalStage(true);
      setPosn({
        ...posn,
        ghostX: posn.ghostX + 100,
        // ghostY: posn.ghostY - 150,
      });
    }, 1000);

    // Send API Calls:
  };

  const chooseMusic = (card) => {
    // send music to the backend
    console.log("CARD", card);
    setPosn({
      ...posn,
      musicCardInitial: 1,
      musicCardFinal: 0,
    });
    setTextContent("");
    setTimeout(() => {
      setTextContent("Now choose a dance!");
      setShowMusicCarousel(false);
      setCarouselContent([
        {
          image: img,
          title: "Hello!",
        },
        {
          image: img,
          title: "Hello!",
        },
        {
          image: img,
          title: "Hello!",
        },
        {
          image: img,
          title: "Hello!",
        },
      ]);
      setshowDanceCarousel(true);
    }, 1000);
    setMusic(card?.title);
    console.log(music);
  };

  const chooseDance = (card) => {
    console.log("CARD", card);
    setPosn({
      ...posn,
      danceCardInitial: 1,
      danceCardFinal: 0,
    });
    setTimeout(() => {
      setshowDanceCarousel(false);
      setTextContent("");
    }, 1000);

    setDance(card?.title);
    finalCall();
  };

  const onFirstSubmit = (textContent) => {
    setKeyboardShown({ status: false });
    setTextContent("");
    setPosn({
      ...posn,
      ghostX: posn.ghostX + 10,
      ghostY: posn.ghostY - 150,
      textInitial: 1,
      textFinal: 0,
    });
    // API CALL
    setEmotion(emotion);
    console.log(textContent);
    setTimeout(() => {
      setTextContent(
        "Great! I've got what you need for some good nostalgia! Now tell me, what song would you like to listen?"
      );
      setPosn({
        ...posn,
        ghostX: posn.ghostX + 10,
        ghostY: posn.ghostY - 150,
        textInitial: 0,
        textFinal: 1,
      });

      setCarouselContent([
        {
          image: img,
          title: "Beat_It",
        },
        {
          image: img,
          title: "Rehab",
        },

        {
          image: img,
          title: "Someone_Like_You",
        },
        {
          image: img,
          title: "Smells_Like_Teen_Spirit",
        },
      ]);
      setShowMusicCarousel(true);
    }, 500);
  };

  return (
    <PosnContext.Provider value={[posn, setPosn]}>
      <div className={isFinalStage ? "final-stage-bg App" : "App"}>
        <header className="App-header">
          <img src={logo} alt="Logo" className="App-logo" />{" "}
          <span
            style={{
              padding: 20,
              fontSize: 40,
              fontFamily: "Bungee Shade",
              color: "#f000ff",
              textShadow: "5px 4px 10px rgba(255, 254, 254, 0.4)",
            }}
          >
            ReLive
          </span>
          <img
            src={disco}
            style={{ height: 220, position: "absolute", top: 0, right: 80 }}
          />
        </header>
        <Ghost textContent={textContent} />
        {showMusicCarousel ? (
          <CarouselContainer
            content={carouselContent}
            onPress={chooseMusic}
            scaleInitial={posn.musicCardInitial}
            scaleFinal={posn.musicCardFinal}
          />
        ) : null}
        {showDanceCarousel ? (
          <CarouselContainer
            content={carouselContent}
            onPress={chooseDance}
            scaleInitial={posn.danceCardInitial}
            scaleFinal={posn.danceCardFinal}
          />
        ) : null}
        {isFinalStage && (
          <FinalPage
            setTextContent={setTextContent}
            emotion={emotion}
            music={music}
            dance={dance}
          />
        )}
        {keyboardShown.status && (
          <ChatInput keyboardShown={keyboardShown} onSubmit={onFirstSubmit} />
        )}
      </div>
    </PosnContext.Provider>
  );
};

export default App;
