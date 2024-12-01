"use client";
import { useState } from "react";
import remarkGfm from "remark-gfm";
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

  return (
    <Container maxW="100vw">
      <VStack spacing={8}>
        <Heading as="h1" size="xl" color="gray.800">
          AI-Powered LinkedIn Post Curation
        </Heading>
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={8} w="full">
          <Card>
            <CardHeader>
              <Heading size="md" display="flex" alignItems="center" gap={2}>
                <FileText size={20} />
                Input Transcript
              </Heading>
            </CardHeader>
            <CardBody>
              <VStack spacing={4}>
                <Textarea
                  placeholder="Paste your video/blog transcript here..."
                  value={transcript}
                  onChange={(e) => setTranscript(e.target.value)}
                  minH="300px"
                  resize="vertical"
                />
                <Text fontSize="sm" color="gray.500" alignSelf="flex-start">
                  {transcript.length} characters |{" "}
                  {transcript.split(/\s+/).filter(Boolean).length} words
                </Text>
              </VStack>
            </CardBody>
            <CardFooter justify="space-between">
              <Select
                icon={<Brain size={16} />}
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                w="180px"
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
                leftIcon={<Send size={16} />}
              >
                Generate Post
              </Button>
            </CardFooter>
          </Card>
          <Card>
            <CardHeader>
              <Heading size="md" display="flex" alignItems="center" gap={2}>
                <Sparkles size={20} />
                Generated Post
              </Heading>
            </CardHeader>
            <CardBody>
              {error ? (
                <Text color="red.500">{error}</Text>
              ) : generatedPost ? (
                <Box
                  bg="white"
                  borderWidth="1px"
                  borderRadius="md"
                  p={4}
                  minH="300px"
                  whiteSpace="pre-wrap"
                >
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
                    {generatedPost}
                  </ReactMarkdown>
                </Box>
              ) : (
                <Box textAlign="center" color="gray.400" minH="300px">
                  Generated post will appear here
                </Box>
              )}
            </CardBody>
            {generatedPost && (
              <CardFooter justify="flex-end" gap={2}>
                <Button
                  onClick={handleCopy}
                  variant="outline"
                  leftIcon={<Copy size={16} />}
                >
                  Copy to Clipboard
                </Button>
                <Button
                  onClick={() => {
                    setGeneratedPost("");
                    setError("");
                  }}
                  variant="outline"
                  leftIcon={<RefreshCw size={16} />}
                >
                  Retry Generation
                </Button>
              </CardFooter>
            )}
          </Card>
        </SimpleGrid>
      </VStack>
    </Container>
  );
}
