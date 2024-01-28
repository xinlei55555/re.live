import React, { useState } from "react";
import Slider from "react-slick";
import { FaArrowRight, FaArrowLeft } from "react-icons/fa";
import "./CarouselContainer.css";
import { motion } from "framer-motion";

const Card = ({ card, onPress }) => {
  return (
    <div
      className="card"
      onClick={() => {
        onPress(card);
      }}
    >
      <img src={card?.image} alt={card?.title} style={{}} />
      <div style={{ fontWeight: "bold", height: 50 }}>
        <p style={{ fontWeight: "bold" }}>{card?.title}</p>
      </div>
    </div>
  );
};

const NextArrow = ({ onClick }) => {
  return (
    <div className="arrow next" onClick={onClick}>
      <FaArrowRight />
    </div>
  );
};

const PrevArrow = ({ onClick }) => {
  return (
    <div className="arrow prev" onClick={onClick}>
      <FaArrowLeft />
    </div>
  );
};

export const CarouselContainer = ({
  content,
  onPress,
  scaleInitial,
  scaleFinal,
}) => {
  const [imageIndex, setImageIndex] = useState(0);

  const settings = {
    infinite: true,
    lazyLoad: true,
    speed: 300,
    slidesToShow: 3,
    centerMode: true,
    centerPadding: 0,
    nextArrow: <NextArrow />,
    prevArrow: <PrevArrow />,
    beforeChange: (current, next) => setImageIndex(next),
  };

  return (
    <motion.div
      animate={{ scale: [scaleInitial, scaleFinal] }}
      transition={{
        time: [0, 1],
        duration: 1,
        // repeat: Infinity,
        type: "keyframes",
        ease: "easeInOut",
      }}
    >
      <Slider {...settings}>
        {content.map((card, idx) => (
          <div
            className={idx === imageIndex ? "slide activeSlide" : "slide"}
            key={idx}
          >
            <Card card={card} onPress={onPress} />
          </div>
        ))}
      </Slider>
    </motion.div>
  );
};
