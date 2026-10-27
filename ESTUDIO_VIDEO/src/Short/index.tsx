import { Caption, createTikTokStyleCaptions, TikTokPage } from "@remotion/captions";
import React, { useMemo } from "react";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  interpolate,
  OffthreadVideo,
  Sequence,
  Series,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Montserrat";

// Heavy, readable, and it has accents (é, ç, ñ, ü...).
const { fontFamily: FONT } = loadFont("normal", { weights: ["900"], subsets: ["latin", "latin-ext"] });

type Range = { fromMs: number; toMs: number };

export type ShortProps = {
  video: string; // file in public/, e.g. "take.mp4"
  captions: string; // its word timings in public/, e.g. "take.json"
  accent: string; // brand color, e.g. "#FFD400"
  ranges: Range[]; // the kept parts of the take, in source ms, in order
  hook: { text: string; seconds: number } | null; // *word* = accent marker
  callouts: { text: string; atMs: number }[]; // atMs = source ms of the word
  showCaptions?: boolean; // default true; false for a long video that gets an .srt instead
  words?: Caption[]; // filled by calculateShortMetadata, in output ms
};

const FPS = 30;
const toFrame = (ms: number) => Math.round((ms / 1000) * FPS);

const captionBox = (width: number, height: number) =>
  width > height
    ? { top: 800, left: 260, width: 1400, height: 180 }
    : { top: 1150, left: 60, width: 780, height: 260 };

// 2-frame audio fade at both ends of a kept range, so a cut never clicks.
const fade = (f: number, frames: number) =>
  frames < 6 ? 1 : interpolate(f, [0, 2, frames - 3, frames - 1], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

// Where each kept range lands in the output.
const layout = (ranges: Range[]) => {
  let at = 0;
  return ranges.map((r) => {
    const from = toFrame(r.fromMs);
    const frames = Math.max(1, toFrame(r.toMs) - from);
    const part = { ...r, from, frames, at, shiftMs: ((at - from) / FPS) * 1000 };
    at += frames;
    return part;
  });
};

// Source ms -> output ms, or null when that moment was cut.
const toOutputMs = (ms: number, parts: ReturnType<typeof layout>) => {
  const p = parts.find((p) => ms >= p.fromMs && ms < p.toMs);
  return p ? ms + p.shiftMs : null;
};

export const calculateShortMetadata: CalculateMetadataFunction<ShortProps> = async ({ props }) => {
  const parts = layout(props.ranges);
  const raw = (await (await fetch(staticFile(props.captions))).json()) as Caption[];
  const words = raw.flatMap((w) => {
    const p = parts.find((p) => w.startMs >= p.fromMs && w.startMs < p.toMs);
    if (!p) return [];
    const end = Math.min(w.endMs, p.toMs);
    return [{ ...w, startMs: w.startMs + p.shiftMs, endMs: end + p.shiftMs, timestampMs: null }];
  });
  return {
    fps: FPS,
    durationInFrames: Math.max(1, parts.reduce((n, p) => n + p.frames, 0)),
    props: { ...props, words },
  };
};

export const Short: React.FC<ShortProps> = ({ video, accent, ranges, hook, callouts, showCaptions = true, words = [] }) => {
  const parts = useMemo(() => layout(ranges), [ranges]);
  const { pages } = useMemo(
    () => createTikTokStyleCaptions({ captions: words, combineTokensWithinMilliseconds: 600 }),
    [words],
  );
  // Punch-in: the framing alternates on each cut; pieces under 0.8 s keep the previous one.
  const zooms = useMemo(() => {
    let z = 1;
    return parts.map((p, i) => {
      if (i > 0 && p.frames >= toFrame(800)) z = z === 1 ? 1.12 : 1;
      return z;
    });
  }, [parts]);

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Series>
        {parts.map((p, i) => (
          <Series.Sequence key={i} durationInFrames={p.frames}>
            <AbsoluteFill style={{ transform: `scale(${zooms[i]})` }}>
              <OffthreadVideo
                src={staticFile(video)}
                trimBefore={p.from}
                volume={(f) => fade(f, p.frames)}
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
            </AbsoluteFill>
          </Series.Sequence>
        ))}
      </Series>

      {(showCaptions ? pages : []).map((page, i) => {
        const next = pages[i + 1];
        const from = toFrame(page.startMs);
        const until = toFrame(next ? next.startMs : page.startMs + page.durationMs);
        if (until <= from) return null;
        return (
          <Sequence key={i} from={from} durationInFrames={until - from}>
            <CaptionPage page={page} accent={accent} />
          </Sequence>
        );
      })}

      {callouts.map((c, i) => {
        const at = toOutputMs(c.atMs, parts);
        if (at === null) return null;
        return (
          <Sequence key={i} from={toFrame(at)} durationInFrames={toFrame(1200)}>
            <Callout text={c.text} accent={accent} frames={toFrame(1200)} />
          </Sequence>
        );
      })}

      {hook ? (
        <Sequence durationInFrames={toFrame(hook.seconds * 1000)}>
          <HookCard text={hook.text} accent={accent} frames={toFrame(hook.seconds * 1000)} />
        </Sequence>
      ) : null}

      <ProgressBar accent={accent} />
    </AbsoluteFill>
  );
};

const CaptionPage: React.FC<{ page: TikTokPage; accent: string }> = ({ page, accent }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const box = captionBox(width, height);
  const now = page.startMs + (frame / fps) * 1000;
  const pop = spring({ frame, fps, config: { damping: 200 }, durationInFrames: 4 });
  const fontSize = Math.min(110, Math.floor(box.width / (page.text.trim().length * 0.72)));
  return (
    <AbsoluteFill style={{ ...box, justifyContent: "center", alignItems: "center" }}>
      <div
        style={{
          fontFamily: FONT,
          fontSize,
          lineHeight: 1.05,
          maxWidth: "100%",
          textAlign: "center",
          textTransform: "uppercase",
          color: "white",
          WebkitTextStroke: "18px black",
          paintOrder: "stroke",
          transform: `scale(${0.85 + 0.15 * pop})`,
        }}
      >
        {page.tokens.map((t, i) => (
          <span key={i} style={{ whiteSpace: "pre", color: now >= t.fromMs && now < t.toMs ? accent : "white" }}>
            {t.text}
          </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const HookCard: React.FC<{ text: string; accent: string; frames: number }> = ({ text, accent, frames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 14 }, durationInFrames: 10 });
  const exit = interpolate(frame, [frames - 6, frames], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ top: "12%", bottom: undefined, height: "auto", alignItems: "center" }}>
      <div
        style={{
          background: "white",
          color: "black",
          fontFamily: FONT,
          fontSize: 76,
          lineHeight: 1.1,
          textTransform: "uppercase",
          textAlign: "center",
          maxWidth: "84%",
          padding: "28px 40px",
          borderRadius: 28,
          boxShadow: "0 12px 40px rgba(0,0,0,0.35)",
          transform: `scale(${0.6 + 0.4 * enter})`,
          opacity: Math.min(enter, exit),
        }}
      >
        {text.split(/(\*[^*]+\*)/).filter(Boolean).map((part, i) =>
          part.startsWith("*") ? (
            <span key={i} style={{ background: accent, borderRadius: 10, padding: "0 12px" }}>
              {part.slice(1, -1)}
            </span>
          ) : (
            <span key={i}>{part}</span>
          ),
        )}
      </div>
    </AbsoluteFill>
  );
};

const Callout: React.FC<{ text: string; accent: string; frames: number }> = ({ text, accent, frames }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const pop = spring({ frame, fps, config: { damping: 12 }, durationInFrames: 8 });
  const exit = interpolate(frame, [frames - 5, frames], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const wide = width > height;
  const fontSize = Math.min(wide ? 180 : 240, Math.floor((width * (wide ? 0.35 : 0.8)) / (text.length * 0.72)));
  return (
    <AbsoluteFill
      style={
        wide
          ? { top: "10%", left: "60%", width: "36%", bottom: undefined, height: "auto", alignItems: "center" }
          : { top: "26%", bottom: undefined, height: "auto", alignItems: "center" }
      }
    >
      <div
        style={{
          fontFamily: FONT,
          fontSize,
          textTransform: "uppercase",
          color: accent,
          WebkitTextStroke: "24px black",
          paintOrder: "stroke",
          transform: `scale(${0.5 + 0.5 * pop})`,
          opacity: exit,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

const ProgressBar: React.FC<{ accent: string }> = ({ accent }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        height: 10,
        width: `${(frame / Math.max(1, durationInFrames - 1)) * 100}%`,
        background: accent,
      }}
    />
  );
};
