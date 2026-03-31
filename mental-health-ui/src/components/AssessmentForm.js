import React, { useState } from "react";
import axios from "axios";
import "../styles/assessment.css";

import {
  Editor,
  EditorProvider,
  Toolbar,
  BtnBold,
  BtnItalic,
  BtnUnderline,
  BtnBulletList,
  BtnNumberedList
} from "react-simple-wysiwyg";

const questions = [
  "Little interest or pleasure in doing things",
  "Feeling down, depressed, or hopeless",
  "Trouble sleeping",
  "Feeling tired or having little energy",
  "Poor appetite or overeating",
  "Feeling bad about yourself",
  "Trouble concentrating",
  "Moving or speaking slowly",
  "Thoughts of self-harm or suicide"
];

const AssessmentForm = ({ onResult }) => {
  const [answers, setAnswers] = useState(Array(9).fill(""));
  const [loading, setLoading] = useState(false);

  const handleChange = (index, value) => {
    const updated = [...answers];
    updated[index] = value;
    setAnswers(updated);
  };

  const cleanHTML = (html) => {
    return html.replace(/<[^>]+>/g, "").trim();
  };

  const handleSubmit = async () => {
    if (answers.some(a => cleanHTML(a) === "")) {
      alert("Please answer all questions");
      return;
    }

    setLoading(true);

    try {
      const cleanedAnswers = answers.map(a => cleanHTML(a));

      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/api/v1/phq9/submit`,
        {
            user_id: "user_ai_2",
            answers_text: cleanedAnswers
        }
        );

      onResult(response.data);

    } catch (error) {
      console.error(error);
      alert("Error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="title">PHQ-9 Assessment</h2>

      {questions.map((q, index) => (
        <div className="card" key={index}>

          <div className="question">
            {index + 1}. {q}
          </div>

          {/* ✅ FIX: Separate Provider per Editor */}
          <div className="editor-container">
            <EditorProvider>
              <Editor
                value={answers[index]}
                onChange={(e) => handleChange(index, e.target.value)}
              >
                <Toolbar>
                  <BtnBold />
                  <BtnItalic />
                  <BtnUnderline />
                  <BtnBulletList />
                  <BtnNumberedList />
                </Toolbar>
              </Editor>
            </EditorProvider>
          </div>

        </div>
      ))}

      <button className="button" onClick={handleSubmit}>
        {loading ? "Analyzing..." : "Analyze with AI"}
      </button>
    </div>
  );
};

export default AssessmentForm;