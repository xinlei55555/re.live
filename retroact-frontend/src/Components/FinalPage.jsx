import React, { useEffect, useState, useRef } from "react";
import vinyl from "./vinyl.gif";
import xl from "./XL.gif";
import "./FinalPage.css";
import { motion } from "framer-motion";

const Polaroid = ({ thumbnail, emotion, backImage, constraintsRef }) => {
  return (
    <motion.div className="polaroid" drag dragConstraints={constraintsRef}>
      <div className="polaroid-inner">
        <div className="front">
          <img
            src={thumbnail} // Front image (GIF)
            alt="polaroid front"
            style={{ width: 200, height: 200 }}
            className={
              emotion === "energetic" ? "neon-effect" : "soothing-effect"
            }
          />
        </div>
        <div className="back">
          <img
            style={{ width: 225, height: 225 }}
            src={backImage} // Back image
            alt="polaroid back"
          />
        </div>
      </div>
    </motion.div>
  );
};

export const FinalPage = ({ setTextContent, music, dance, emotion }) => {
  const [showGallery, setShowGallery] = useState(false);
  const [galleryImages, setGalleryImages] = useState([
    { original: vinyl, thumbnail: xl },
    { original: vinyl, thumbnail: xl },
    { original: vinyl, thumbnail: xl },
    { original: vinyl, thumbnail: xl },
    { original: vinyl, thumbnail: xl },
    { original: vinyl, thumbnail: xl },
  ]);
  const constraintsRef = useRef(null);
  useEffect(() => {
    setTextContent(
      "Getting things ready for you... Get your volume up and ready :)"
    );
    setTimeout(() => {
      setTextContent("Welcome to the past in 3, 2, 1...");
      setTimeout(() => {
        setShowGallery(true);
        setTextContent("Here we go!");
      }, 3000);
    }, 5200);
  }, []);

  return (
    <motion.div
      animate={{ scale: [0, 1] }}
      transition={{
        time: [0, 1],
        duration: 1,
        // repeat: Infinity,
        type: "keyframes",
        ease: "easeInOut",
      }}
    >
      <motion.div className="gallery-original" ref={constraintsRef}>
        {showGallery &&
          galleryImages.map((card, index) => {
            return (
              <Polaroid
                key={index}
                thumbnail={card.thumbnail}
                emotion={emotion}
                backImage={card.original}
                constraintsRef={constraintsRef}
              />
            );
          })}
      </motion.div>
      {!showGallery && (
        <img
          src={vinyl}
          alt="loading..."
          style={{ height: 550 }}
          className={showGallery ? "fade-out" : "image-visible"}
        />
      )}
    </motion.div>
  );
};
