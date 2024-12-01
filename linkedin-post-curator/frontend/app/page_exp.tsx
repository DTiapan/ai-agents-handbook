"use client";
import showdown from "showdown";
// Remove the duplicate import statement for ReactMarkdown
// import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useState } from "react";
import {
  Button,
  Textarea,
  Box,
  Heading,
  Select,
  useToast,
  VStack,
  Text,
  Container,
  SimpleGrid,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
} from "@chakra-ui/react";
import ReactMarkdown from "react-markdown";
import { FileText, Brain, Send, Copy, RefreshCw, Sparkles } from "lucide-react";
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
export default function PostCurationApp() {
  const [transcript, setTranscript] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedPost, setGeneratedPost] = useState("");
  const [error, setError] = useState("");
  const [selectedModel, setSelectedModel] = useState("llama3.2");
  const toast = useToast();
  const handleGenerate = async () => {
    setIsGenerating(true);
    setError("");
    try {
      const response = await fetch(`${API_URL}/process-content`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({ transcript, model: selectedModel }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.status === "success" && data.result) {
        setGeneratedPost(data.result.raw);
      } else {
        setError(data.message || "Failed to generate post. Please try again.");
      }
    } catch (err) {
      setError(
        `An error occurred: ${
          err instanceof Error ? err.message : "Unknown error"
        }`
      );
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedPost);
    toast({
      title: "Copied to clipboard",
      status: "success",
      duration: 2000,
      isClosable: true,
    });
  };

  const markdownText = `
  # Jeff Bezos' Journey to Success
  
  - Born in Albuquerque, New Mexico, and raised in Houston, Texas, and Miami, Florida, setting the stage for his future endeavors.
  - Academic foundation at Princeton University, where he earned degrees in electrical engineering and computer science, laying the groundwork for his future success.
  
  **A Wall Street Connection**
  
  - Before starting Amazon, Bezos worked on Wall Street, gaining valuable experience that would shape the company's success.
  - This experience would later prove instrumental in developing Amazon's business model and driving its growth.
  
  ## Revolutionizing E-commerce
  
  - In 1994, Bezos founded Amazon, pioneering e-commerce and transforming the way people shop.
    `;

  return (
    <Box borderWidth="1px" borderRadius="md" p={4} bg="gray.50">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: (props) => <Heading as="h1" size="2xl" {...props} />,
          h2: (props) => <Heading as="h2" size="xl" {...props} />,
          h3: (props) => <Heading as="h3" size="lg" {...props} />,
          h4: (props) => <Heading as="h4" size="md" {...props} />,
          h5: (props) => <Heading as="h5" size="sm" {...props} />,
          h6: (props) => <Heading as="h6" size="xs" {...props} />,
          p: (props) => <Text {...props} />,
        }}
      >
        {markdownText}
      </ReactMarkdown>
    </Box>
  );
}
