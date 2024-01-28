import React from "react";
import { motion } from "framer-motion";
import "./AnimatedTextBox.css";
export const AnimatedTextBox = ({ textContent }) => {
  return (
    <motion.div className="AnimatedTextBox">
      <p className="text">{textContent}</p>
    </motion.div>
  );
};
