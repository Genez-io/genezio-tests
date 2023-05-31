import { ChatCompletionRequestMessage, Configuration, OpenAIApi, ChatCompletionRequestMessageRoleEnum, CreateChatCompletionResponse } from "openai";
import mongoose from "mongoose"
import * as dotenv from 'dotenv';
dotenv.config();

const OPENAI_MODEL_GPT3_5 = 'gpt-3.5-turbo';
const OPENAI_MODEL_GPT_4 = 'gpt-4';
const OPENAI_MODEL_DAVINCI = 'text-davinci-003';
const MONGODB_URI =
    "mongodb+srv://genezio:genezio@cluster0.c6qmwnq.mongodb.net/?retryWrites=true&w=majority";

const characters: { [name: string]: string } = {
  "yoda": "Respond to me as if you are Yoda from Star Wars:",
  "chewbacca": "Respond to me as if you are Chewbacca from Star Wars: "
};


export class ChatBackend {
  openai: OpenAIApi | undefined = undefined;

  constructor() {
    this.#connect();
    const configuration = new Configuration({
      apiKey: process.env.OPENAPI_KEY
    });
    const openai = new OpenAIApi(configuration);
    this.openai = openai;
  }

  /**
   * Private method used to connect to the DB.
   */
  #connect() {
    mongoose.connect(MONGODB_URI!).catch((e) => {
      console.log(`Error connecting to database: ${e}`);
      throw e;
    });
  }

  async askChatGpt(prompt: string, question: string): Promise<string> {
    // Create a list of messages (that contains only one message)
    const my_msg: ChatCompletionRequestMessage[] = [
      {
        content: prompt,
        role: ChatCompletionRequestMessageRoleEnum.System
      },
      {
        content: question,
        role: ChatCompletionRequestMessageRoleEnum.User
      },
    ];

    let chat: any;
    try {
      // Create a chat OpenAI instance
      chat = await this.openai!.createChatCompletion({
        model: OPENAI_MODEL_GPT3_5,
        messages: my_msg,
      });
    } catch (e) {
      console.log(`Error creating chat: ${e}`);
      throw e;
    }

    // Return the response from chatGPT
    return chat.data.choices[0].message.content;
  }

  async askYoda(question: string): Promise<string> {
    return this.askChatGpt(characters["yoda"]!, question);
  }

  async askChewbacca(question: string): Promise<string> {
    return this.askChatGpt(characters["chewbacca"]!, question);
  }

  async addBookmark(content: string): Promise<string> {
    console.log(`Trying to add bookmark with content: ${content}`);

    // Check if bookmark already exists
    const value = await mongoose.connection.db.collection("bookmarks").findOne({ content });
    if (value !== null) {
      console.log("Bookmark already exists");
      throw "Bookmark already exists";
    }

    // Add bookmark into the database
    await mongoose.connection.db.collection("bookmarks").insertOne({ content }).catch((e) => {
      console.log(`Error adding bookmark: ${e}`);
      throw e;
    });

    return "success";
  }

  async getAllBookmarks(): Promise<string[]> {
    // Get all the bookmarks from the database
    const rawBookmarks = await mongoose.connection.db.collection("bookmarks").find().toArray();

    // Check if there are any bookmarks
    if (rawBookmarks === null) {
      return [];
    }

    // Convert the list of bookmarks into a list of strings List<string>
    const bookmarksList = rawBookmarks.map((element) => element.content.toString());

    return bookmarksList;
  }
}
