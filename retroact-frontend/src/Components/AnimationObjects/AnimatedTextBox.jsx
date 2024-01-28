import React, { useContext, useEffect, useState } from "react";
import { motion, useAnimation } from "framer-motion";
import WriteLikeChatGPT from "write-like-chat-gpt";
import "./AnimatedTextBox.css";
import { PosnContext } from "../../App";
export const AnimatedTextBox = ({ textContent }) => {
  const [posn, setPosn] = useContext(PosnContext);
  const [textVisible, setTextVisible] = useState(false);
  const controls = useAnimation();
  useEffect(() => {
    controls
      .start({
        scale: [posn.textInitial, posn.textFinal],
        transition: {
          time: [0, 1],
          duration: 1,
          type: "keyframes",
          ease: "easeInOut",
        },
      })
      .then(() => {
        console.log("DONE!");
        posn.textFinal === 1 && setTextVisible(true);
      });
  }, [controls, posn.textInitial, posn.textFinal]);

  return (
    <motion.div className="AnimatedTextBox" animate={controls}>
      {textVisible && (
        <p className="text">
          <WriteLikeChatGPT text={textContent} />
        </p>
      )}
    </motion.div>
  );
};
