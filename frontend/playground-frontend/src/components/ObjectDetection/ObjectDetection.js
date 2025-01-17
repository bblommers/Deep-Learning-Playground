import React, { useState, useMemo } from "react";
import ImageFileUpload from "../general/ImageFileUpload";
import { OBJECT_DETECTION_PROBLEM_TYPES } from "../../settings";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { FormControlLabel, Switch } from "@mui/material";
import {
  Input,
  TitleText,
  BackgroundLayout,
  TrainButton,
  Results,
  ChoiceTab,
  Spacer,
  CustomModelName,
} from "../index";

const ObjectDetection = () => {
  const [customModelName, setCustomModelName] = useState(
    `Model ${new Date().toLocaleString()}`
  );
  const [problemType, setProblemType] = useState("");
  const [dlpBackendResponse, setDLPBackendResponse] = useState();
  const [beginnerMode, setBeginnerMode] = useState(true);
  const [inputKey, setInputKey] = useState(0);
  const [uploadFile, setUploadFile] = useState(null);

  const input_responses = {
    problemType: problemType?.value,
    uploadFile: uploadFile,
  };

  const input_queries = [
    {
      queryText: "ProblemType",
      options: OBJECT_DETECTION_PROBLEM_TYPES,
      onChange: setProblemType,
      defaultValue: problemType,
    },
  ];

  const ResultMemo = useMemo(
    () => (
      <Results
        dlpBackendResponse={dlpBackendResponse}
        problemType={OBJECT_DETECTION_PROBLEM_TYPES[0]}
        choice="objectdetection"
      />
    ),
    [dlpBackendResponse, OBJECT_DETECTION_PROBLEM_TYPES[0]]
  );

  const onClick = () => {
    setBeginnerMode(!beginnerMode);
    setInputKey((e) => e + 1);
  };

  return (
    <div id="ml-models">
      <DndProvider backend={HTML5Backend}>
        <div className="d-flex flex-row justify-content-between">
          <FormControlLabel
            control={<Switch id="mode-switch" onClick={onClick}></Switch>}
            label={`${beginnerMode ? "Enable" : "Disable"} Advanced Settings`}
          />
          <CustomModelName
            customModelName={customModelName}
            setCustomModelName={setCustomModelName}
          />
          <ChoiceTab />
        </div>
        <BackgroundLayout>
          <div className="input-container d-flex flex-column align-items-center justify-content-center">
            <ImageFileUpload
              uploadFile={uploadFile}
              setUploadFile={setUploadFile}
            />
          </div>
          <TrainButton
            {...input_responses}
            setDLPBackendResponse={setDLPBackendResponse}
            choice="objectdetection"
          />
        </BackgroundLayout>
      </DndProvider>
      <Spacer height={40} />

      <TitleText text="Detection Parameters" />
      <BackgroundLayout>
        {input_queries.map((e) => (
          <Input {...e} key={e.queryText + inputKey} />
        ))}
      </BackgroundLayout>

      <Spacer height={40} />
      <TitleText text="Detection Results" />
      {ResultMemo}
    </div>
  );
};

export default ObjectDetection;
