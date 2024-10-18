import { useCompletion } from "@ai-sdk/react";
import Markdown from "react-markdown";

const Chat = () => {
  const { completion, input, handleInputChange, handleSubmit, isLoading } =
    useCompletion({
      api: import.meta.env.VITE_CHAT_API_URL,
    });
  return (
    <div className="h-[100vh] w-[90vw] flex justify-center items-center bg-white">
      <div className="rounded-xl flex flex-col h-[90vh] w-[80vw]">
        <div className="flex-grow">
          {completion && (
            <div>
              <div className="flex gap-2 ">
                <div className="bg-gray-100 rounded-full p-1 h-8 w-8 text-center text-gray-400 mt-3">
                  AI
                </div>
                <Markdown
                  className={`prose lg:prose-xl p-4 my-2 text-gray-600 bg-gray-100 rounded-lg`}
                >
                  {completion}
                </Markdown>
              </div>
            </div>
          )}
        </div>
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            className={`rounded-xl h-20 mb-10 mt-3 w-full bg-gray-100 px-4 text-gray-600 placeholder:text-gray-400 focus:outline-none ${
              isLoading ? "animate-pulse" : ""
            }`}
            name="prompt"
            value={input}
            onChange={handleInputChange}
            placeholder="Essay Topic"
            disabled={isLoading}
          />
        </form>
      </div>
    </div>
  );
};

export default Chat;
