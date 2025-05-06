'use client'
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useStore } from '@/app/store/useStore';

export default function SplitExpenses() {
  const { user, currentGroup, setUser, addExpense, fetchProtectedData, initializeWebSocket } = useStore();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        await fetchProtectedData();
        initializeWebSocket();
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      }
    };

    loadData();

    // Cleanup WebSocket subscriptions when component unmounts
    return () => {
      // In a real app, we would unsubscribe from WebSocket events here
      // For now, the WebSocket service handles cleanup internally
    };
  }, [fetchProtectedData, initializeWebSocket]);

  return (
    <div className="grid grid-rows-[auto_1fr_auto] items-center justify-items-center min-h-screen p-8 pb-20 gap-8 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <motion.header
        className="w-full text-center"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Link href="/" className="text-blue-500 mb-2 inline-block">← Back to Home</Link>
        <h1 className="text-3xl font-bold mb-2">Split Expenses</h1>
        <p className="text-gray-600 dark:text-gray-400">Calculate who owes what</p>
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
          <h2 className="text-xl font-semibold mb-4">New Expense</h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Description</label>
              <input
                type="text"
                placeholder="Dinner, Groceries, etc."
                className="w-full p-2 border rounded-md dark:bg-gray-700 dark:border-gray-600"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Amount</label>
              <input
                type="number"
                placeholder="0.00"
                className="w-full p-2 border rounded-md dark:bg-gray-700 dark:border-gray-600"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Paid by</label>
              <select className="w-full p-2 border rounded-md dark:bg-gray-700 dark:border-gray-600">
                <option>Select a person</option>
                <option>John</option>
                <option>Sarah</option>
                <option>Mike</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Split between</label>
              <div className="space-y-2">
                <div className="flex items-center">
                  <input type="checkbox" id="person1" className="mr-2" />
                  <label htmlFor="person1">John</label>
                </div>
                <div className="flex items-center">
                  <input type="checkbox" id="person2" className="mr-2" />
                  <label htmlFor="person2">Sarah</label>
                </div>
                <div className="flex items-center">
                  <input type="checkbox" id="person3" className="mr-2" />
                  <label htmlFor="person3">Mike</label>
                </div>
              </div>
            </div>

            <motion.button
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md transition-colors"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Add Expense
            </motion.button>
          </div>
        </motion.div>

        <motion.div
          className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md w-full"
          initial={{ scale: 0.95 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.3, delay: 0.4 }}
        >
          <h2 className="text-xl font-semibold mb-4">Settlement Summary</h2>
          <div className="space-y-3">
            <div className="p-3 bg-gray-100 dark:bg-gray-700 rounded-md">
              <p className="font-medium">John owes Sarah $15.50</p>
            </div>
            <div className="p-3 bg-gray-100 dark:bg-gray-700 rounded-md">
              <p className="font-medium">Mike owes Sarah $22.75</p>
            </div>
          </div>
        </motion.div>
      </motion.main>

      <motion.footer
        className="flex gap-[24px] flex-wrap items-center justify-center mt-8"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.5 }}
      >
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Split Wisely - Split expenses with friends and family
        </p>
      </motion.footer>
    </div>
  );
} 