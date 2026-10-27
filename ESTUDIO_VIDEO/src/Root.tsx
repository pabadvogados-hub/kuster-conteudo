import { Composition, staticFile } from "remotion";
import {
  CaptionedVideo,
  calculateCaptionedVideoMetadata,
  captionedVideoSchema,
} from "./CaptionedVideo";
import { calculateShortMetadata, Short } from "./Short";

const editDefaults = {
  video: "take.mp4",
  captions: "take.json",
  accent: "#1F6FEB", // cor da marca do escritorio - trocar em config/marca.json e aqui
  ranges: [],
  hook: null,
  callouts: [],
};

// Each <Composition> is an entry in the sidebar!

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="CaptionedVideo"
        component={CaptionedVideo}
        calculateMetadata={calculateCaptionedVideoMetadata}
        schema={captionedVideoSchema}
        width={1080}
        height={1920}
        defaultProps={{
          src: staticFile("take.mp4"),
        }}
      />
      <Composition
        id="Short"
        component={Short}
        calculateMetadata={calculateShortMetadata}
        width={1080}
        height={1920}
        defaultProps={editDefaults}
      />
      <Composition
        id="Wide"
        component={Short}
        calculateMetadata={calculateShortMetadata}
        width={1920}
        height={1080}
        defaultProps={editDefaults}
      />
    </>
  );
};
