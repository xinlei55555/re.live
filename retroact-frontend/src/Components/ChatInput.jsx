import React, { useState } from "react";
import { motion } from "framer-motion";
import "./ChatInput.css";

export const ChatInput = ({ keyboardShown, onSubmit }) => {
  //   const [posn, setPosn] = useContext(PosnContext);
  const [text, setText] = useState("");
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
      <form
        onSubmit={() => {
          onSubmit(text);
        }}
      >
        <input
          className="chatInput"
          placeholder="Type your response..."
          value={text}
          onChange={(e) => {
            setText(e.target.value);
          }}
        />
      </form>
    </motion.div>
  );
};
