import React, { useMemo, useRef, useContext } from "react";
// import { Canvas } from "@react-three/fiber";
// import { useFrame } from "@react-three/fiber";
// import { MathUtils } from "three";
// import vertexShader from "./vertexShader";
// import fragmentShader from "./fragment_Shader";
import { PosnContext } from "../../App";
import { motion } from "framer-motion";

import { AnimatedTextBox } from "./AnimatedTextBox";

export default function Ghost() {
  const [posn, setPosn] = useContext(PosnContext);
  console.log(posn);
  // const [x, y] = useMemo(() => [Math.random() * 100, Math.random() * 100], []);
  // const [x, y] = useMemo(() => [Math.random() * 100, Math.random() * 100], []);
  return (
    <motion.div
      className="blob"
      animate={{
        x: posn.x,
        y: posn.y,
      }}
      transition={{
        duration: 3,
      }}
    >
      <motion.svg
        viewBox="0 0 500 500"
        xmlns="http://www.w3.org/2000/svg"
        height="200px"
        // {...props}
      >
        <defs>
          <linearGradient id="a" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#c2e59c" />
            <stop offset="100%" stopColor="#64b3f4" />
          </linearGradient>
        </defs>
        <motion.path
          animate={{ scale: [0.9, 1, 0.9] }}
          transition={{
            time: [0, 1],
            duration: 3,
            repeat: Infinity,
            type: "keyframes",
            ease: "easeInOut",
          }}
          d="M462.5 315q-33.5 65-92 95.5t-125.5 46Q178 472 131 421T58 310q-26-60-2.5-122t72-113.5q48.5-51.5 121-47T368 81q47 49 87.5 109t7 125z"
          fill="url(#a)"
        >
          {/* <motion.animate
            attributeName="d"
            dur="1000ms"
            repeatCount="indefinite"
            "M466,310Q436,370,384.5,401.5Q333,433,275,457Q217,481,166.5,443Q116,405,78.5,358Q41,311,44,250.5Q47,190,70,129.5Q93,69,155,46Q217,23,275.5,44Q334,65,395.5,91Q457,117,476.5,183.5Q496,250,466,310Z"
          ></motion.animate> */}
        </motion.path>
      </motion.svg>
      <AnimatedTextBox textContent={"Hello!"} />
    </motion.div>
  );
}
//
