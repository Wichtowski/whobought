'use client'
import Image from "next/image";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Link from "next/link";

export default function Home() {
  const [showContent, setShowContent] = useState(false);

  useEffect(() => {
    // Show content after a brief delay
    const timer = setTimeout(() => {
      setShowContent(true);
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="grid grid-rows-[auto_1fr_auto] items-center justify-items-center min-h-screen p-8 pb-20 gap-8 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <motion.header
        className="w-full text-center"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold mb-2">Split Wisely</h1>
        <p className="text-gray-600 dark:text-gray-400">Split expenses without the headache</p>
      </motion.header>

      <motion.main
        className="flex flex-col gap-[32px] w-full max-w-3xl"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <motion.div
          className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md w-full"
          initial={{ scale: 0.95 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.3, delay: 0.3 }}
        >
          <h2 className="text-xl font-semibold mb-4">Welcome to Split Wisely!</h2>
          <p className="mb-4 text-gray-600 dark:text-gray-400">
            The easiest way to split expenses with friends, family, or roommates.
            No more awkward money conversations or complicated calculations.
          </p>
          <div className="flex justify-center mb-6">
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Image
                src="/welcome-illustration.png"
                alt="Split expenses illustration"
                width={200}
                height={200}
                className="rounded-md"
              />
            </motion.div>
          </div>
          <Link href="/register">
            <motion.button
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 cursor-pointer rounded-md transition-colors font-medium"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Get Started
            </motion.button>
          </Link>

        </motion.div>
      </motion.main>
    </div>
  );
}