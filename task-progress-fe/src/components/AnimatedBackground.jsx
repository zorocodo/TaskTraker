import { motion } from "framer-motion";

export default function AnimatedBackground() {
  return (
    <div className="background">
      {[...Array(15)].map((_, i) => (
        <motion.div
          key={i}
          className="floating-object"
          animate={{
            y: [0, -30, 0],
            rotate: [0, 180, 360],
          }}
          transition={{
            duration: 6 + i,
            repeat: Infinity,
          }}
        />
      ))}
    </div>
  );
}
