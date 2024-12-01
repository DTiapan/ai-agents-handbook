"use client";

import { useState } from "react";
import { Button, Textarea, Box, Heading } from "@chakra-ui/react";
import { Select } from "@chakra-ui/select";
import { useToast } from "@chakra-ui/toast";
import {
  FileTextIcon,
  BrainIcon,
  SendIcon,
  CopyIcon,
  RefreshCwIcon,
  SparklesIcon,
} from "lucide-react";

export default function PostCurationApp() {
  const [transcript, setTranscript] = useState("");
  const [generatedPost, setGeneratedPost] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState("");
  const [selectedModel, setSelectedModel] = useState("llama3.2");

  const toast = useToast();

  const handleGenerate = async () => {
    setIsGenerating(true);
    setError("");
    try {
      const response = await fetch("/process-content", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ transcript: transcript, model: selectedModel }),
      });

      const data = await response.json();

      if (data.status === "success" && data.result) {
        setGeneratedPost(data.result.raw);
      } else {
        setError("Failed to generate post. Please try again.");
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

  const handleRetry = () => {
    setGeneratedPost("");
    setError("");
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedPost);
    toast({ title: "Copied to clipboard", status: "success" });
  };

  return (
    <Box minH="100vh" bg="gray.100" py={8} px={4}>
      <Box maxW="4xl" mx="auto">
        <Heading as="h1" size="xl" textAlign="center" mb={8} color="gray.800">
          AI-Powered LinkedIn Post Curation
        </Heading>

        <Box display="grid" gap={8} gridTemplateColumns="1fr 1fr">
          <Box borderWidth="1px" borderRadius="md" p={4}>
            <Heading size="md" display="flex" alignItems="center" gap={2}>
              <FileTextIcon size={20} />
              Input Transcript
            </Heading>
            <Textarea
              placeholder="Paste your video/blog transcript here..."
              value={transcript}
              onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                setTranscript(e.target.value)
              }
              size="lg"
              minH="300px"
              my={4}
            />
            <Box fontSize="sm" color="gray.500">
              {transcript.length} characters |{" "}
              {transcript.split(/\s+/).filter(Boolean).length} words
            </Box>

            <Box display="flex" justifyContent="space-between" mt={4}>
              <Select
                value={selectedModel}
                onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
                  setSelectedModel(e.target.value)
                }
                w="180px"
                display="flex"
                alignItems="center"
                gap={2}
                icon={<BrainIcon size={16} />}
              >
                <option value="llama3.2">Llama 3.2</option>
                <option value="gpt3.5">GPT-3.5</option>
                <option value="gpt4">GPT-4</option>
              </Select>

              <Button
                onClick={handleGenerate}
                isLoading={isGenerating}
                loadingText="Generating..."
                colorScheme="blue"
                isDisabled={isGenerating || transcript.length === 0}
              >
                <SendIcon />
                Generate Post
              </Button>
            </Box>
          </Box>

          <Box borderWidth="1px" borderRadius="md" p={4}>
            <Heading size="md" display="flex" alignItems="center" gap={2}>
              <SparklesIcon size={20} />
              Generated Post
            </Heading>

            {error && (
              <Box color="red.500" mb={4}>
                {error}
              </Box>
            )}
            {generatedPost ? (
              <>
                <Box
                  bg="white"
                  borderWidth="1px"
                  borderRadius="md"
                  p={4}
                  minH="300px"
                  mb={4}
                  whiteSpace="pre-wrap"
                >
                  {generatedPost}
                </Box>
                <Box display="flex" justifyContent="flex-end" gap={2}>
                  <Button
                    onClick={handleCopy}
                    variant="outline"
                    colorScheme="gray"
                  >
                    <CopyIcon />
                    Copy to Clipboard
                  </Button>
                  <Button
                    onClick={handleRetry}
                    variant="outline"
                    colorScheme="gray"
                  >
                    <RefreshCwIcon />
                    Retry Generation
                  </Button>
                </Box>
              </>
            ) : (
              <Box textAlign="center" color="gray.400" minH="300px">
                Generated post will appear here
              </Box>
            )}
          </Box>
        </Box>
      </Box>
    </Box>
  );
}
