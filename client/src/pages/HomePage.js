import { Textarea } from "@nextui-org/react";
import { useState } from "react";
import { Progress } from "@nextui-org/react";
import { Card, CardBody } from "@nextui-org/react";
import axios from "axios";
import { Button } from "@nextui-org/react";

// structure of labels
// const labels = [{'label': 'admiration', 'score': 0.029029421508312225}]

function Output({ data }) {
  return (
    <Card className="rounded-md">
      <CardBody className="flex flex-col gap-2 sm:gap-3">
        {data.map((item) => (
          <div key={item.label} className="flex flex-row gap-2 items-center">
            <p className="w-48 text-sm">{item.label}</p>
            <Progress
              classNames={{ base: "pt-0.5" }}
              aria-label="Loading..."
              value={item.score / data[0]["score"]}
              maxValue={1}
            />
          </div>
        ))}
      </CardBody>
    </Card>
  );
}

export default function Home() {
  const [value, setValue] = useState("");
  const [labels, setLabels] = useState();
  const [warning, setWarning] = useState(false);

  function handleSubmit() {
    if (value === "") {
      setWarning(true);
    } else {
      setWarning(false);
      axios
        .post("http://localhost:8000/", { input_text: value })
        .then((res) => {
          let label_dict = JSON.parse(res.data);
          let label = [];
          Object.keys(label_dict).forEach((element) => {
            label.push(label_dict[element]);
          });
          setLabels(label);
        });
    }
  }

  return (
    <>
      <div className="flex w-full justify-center p-4">
        <div className="w-96 flex flex-col gap-4">
          <p className="text-2xl font-bold p-1">Sentiment Analysis Interface</p>
          <Textarea
            minRows={5}
            isInvalid={warning}
            radius="sm"
            isRequired
            label={"Enter text" + (warning ? " (required)" : "")}
            labelPlacement="outside"
            placeholder="Text for sentiment analysis."
            classNames={{ input: "text-sm", label: "text-md p-1" }}
            value={value}
            onValueChange={setValue}
            description="Text to sent for inference."
          />
          <Button
            className="bg-zinc-800 text-zinc-100 font-medium w-24 self-end"
            radius="sm"
            size="md"
            onClick={handleSubmit}
          >
            Submit
          </Button>
          {labels && (
            <div>
              <p className="p-1 font-medium">Inference</p>
              <Output data={labels} />
            </div>
          )}
        </div>
      </div>
    </>
  );
}
