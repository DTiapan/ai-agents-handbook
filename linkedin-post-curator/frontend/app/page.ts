"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Loader2,
  Copy,
  RefreshCw,
  FileText,
  Send,
  Brain,
  Sparkles,
} from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import axios from "axios";

// Configure axios base URL
axios.defaults.baseURL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function PostCurationApp() {
  const [transcript, setTranscript] = useState("");
  const [generatedPost, setGeneratedPost] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState("");
  const [selectedModel, setSelectedModel] = useState("llama3.2");

  const handleGenerate = async () => {
    setIsGenerating(true);
    setError("");
    try {
      const response = await axios.post("/generate-post", {
        transcript,
        model: selectedModel,
      });

      setGeneratedPost(response.data.post);
    } catch (err) {
      setError(
        "An error occurred while generating the post. Please try again."
      );
      console.error(err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleRetry = () => {
    setGeneratedPost("");
    setError("");
    handleGenerate();
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedPost);
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
          AI-Powered LinkedIn Post Curation
        </h1>

        <div className="grid gap-8 md:grid-cols-2">
          {/* Input Card */}
          <Card className="md:col-span-1">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Input Transcript
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Textarea
                placeholder="Paste your video/blog transcript here..."
                value={transcript}
                onChange={(e) => setTranscript(e.target.value)}
                className="min-h-[300px] mb-2"
              />
              <div className="text-sm text-gray-500 mt-2">
                {transcript.length} characters |{" "}
                {transcript.split(/\s+/).filter(Boolean).length} words
              </div>
              <div className="mt-4 flex justify-between items-center">
                <Select value={selectedModel} onValueChange={setSelectedModel}>
                  <SelectTrigger className="w-[180px] flex items-center gap-2">
                    <Brain className="h-4 w-4" />
                    <SelectValue placeholder="Select model" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="llama3.2">Llama 3.2</SelectItem>
                  </SelectContent>
                </Select>
                <Button
                  onClick={handleGenerate}
                  disabled={isGenerating || transcript.length === 0}
                  className={`bg-blue-500 hover:bg-blue-600 text-white transition-all duration-300 ease-in-out ${
                    isGenerating ? "animate-pulse" : ""
                  }`}
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Send className="mr-2 h-4 w-4" />
                      Generate Post
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Generated Post Card */}
          <Card className="md:col-span-1">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="h-5 w-5" />
                Generated Post
              </CardTitle>
            </CardHeader>
            <CardContent>
              {error && <div className="text-red-500 mb-4">{error}</div>}
              {generatedPost ? (
                <>
                  <div className="bg-white border rounded-md p-4 min-h-[300px] mb-4 whitespace-pre-wrap">
                    {generatedPost}
                  </div>
                  <div className="flex justify-end space-x-2 mt-4">
                    <Button
                      onClick={handleCopy}
                      variant="outline"
                      className="text-gray-600 hover:bg-gray-100"
                    >
                      <Copy className="mr-2 h-4 w-4" />
                      Copy to Clipboard
                    </Button>
                    <Button
                      onClick={handleRetry}
                      variant="outline"
                      className="text-gray-600 hover:bg-gray-100"
                    >
                      <RefreshCw className="mr-2 h-4 w-4" />
                      Retry Generation
                    </Button>
                  </div>
                </>
              ) : (
                <div className="flex items-center justify-center min-h-[300px] text-gray-400">
                  Generated post will appear here
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
