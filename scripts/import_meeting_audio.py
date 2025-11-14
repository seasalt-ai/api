"""
It provides a command line interface to:
- create a meeting
- generate an upload URL for audio
- upload the audio
- start the transcription process.

Prerequisites:
- Python 3.8+
- pip install requests

Example usage:
    python import_meeting_audio.py --access-token eyxxx --workspace-id test --wav-path test.wav --wav-name test.wav
"""

import argparse
import logging
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from typing import Optional

import requests

root = logging.getLogger()
root.setLevel("DEBUG")
handler = logging.StreamHandler(sys.stdout)
handler.setLevel("DEBUG")
formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)


def main(args: argparse.Namespace):
    logging.debug("process start")
    meeting_id = _create_meeting(args)
    url = _get_meeting_upload_url(args, meeting_id)
    _upload_audio(args, url)
    _analyze_meeting_audio(args, meeting_id)

    logging.debug("process finished")


def _create_meeting(args: argparse.Namespace) -> str:
    body = {
        "meeting_name": args.meeting_name,
        "channel_type": "PHONE",
        "language": args.meeting_language,
        "start_time": args.meeting_start_time,
    }
    url = f"{args.seameet_url_base}/api/v1/workspaces/{args.workspace_id}/meetings"
    response = _query_backend_service(
        access_token=args.access_token,
        url=url,
        method="POST",
        body=body,
    )
    return response["id"]


def _get_meeting_upload_url(args: argparse.Namespace, meeting_id: str) -> str:
    body = {}
    url_parameters = {"file_name": args.wav_name}
    url = f"{args.seameet_url_base}/api/v1/workspaces/{args.workspace_id}/meetings/{meeting_id}/upload_audio_url"
    response = _query_backend_service(
        access_token=args.access_token,
        url=url,
        method="POST",
        body=body,
        url_parameters=url_parameters,
    )
    return response["upload_audio_url"]


def _upload_audio(args: argparse.Namespace, url: str):

    with open(args.wav_path, "rb") as f:
        response = requests.put(url, data=f)
        response.raise_for_status()

    logging.debug((f"uploaded {args.wav_path} to s3"))


def _analyze_meeting_audio(args: argparse.Namespace, meeting_id: str) -> str:
    body = {
        "meeting_id": meeting_id,
        "channel": 1,
        "audio_start_offset": args.audio_start_offset,
        "audio_format": args.audio_format,
        "audio_sample_rate": args.audio_sample_rate,
        "audio_encoding": args.audio_encoding,
        "scenario": args.scenario,
        "scenario_parameters": {
            "went_to_voicemail": False,
            "contains_recordings": False,
            "spoke_to_agent": False,
            "customer_number": args.customer_number,
            "customer_name": args.customer_name,
            "agent_name": args.agent_name,
            "enable_agent_recognition": args.enable_agent_recognition,
            "direction": args.direction,
        },
        "file_name": args.wav_name,
        "speaker_accounts": [],
        "diarization_options":"by_server",
        "num_speakers": 2,
        "enable_itn": True,
        "enable_punctuation": True,
        "use_existing_audio": args.use_existing_audio,
        "reset_meeting": args.reset_meeting,
        "queue_type": args.queue_type,
    }
    url = f"{args.seameet_url_base}/api/v1/workspaces/{args.workspace_id}/meetings/{meeting_id}/analyze_audio"
    _query_backend_service(
        access_token=args.access_token,
        url=url,
        method="POST",
        body=body,
    )


def _query_backend_service(
    access_token: str,
    url: str,
    method: str,
    body: dict = {},
    headers: dict = {},
    url_parameters: dict = {},
    timeout: Optional[float] = None,
) -> dict:
    start_time = time.time()
    response = None
    try:
        if url_parameters:
            url += "?" + urllib.parse.urlencode(url_parameters)
        final_headers = {
            "accept": r"application/json",
            "Content-Type": r"application/json",
            "Authorization": f"Bearer {access_token}",
        }

        if headers:
            final_headers.update(headers)
        # NOTE: Extend default timeout to wait the Backend API-Server responding.
        # - Especially the post_final_transcription is taking too long.
        session = requests.Session()
        request = requests.Request(method, url, json=body, headers=final_headers)
        response = session.send(request.prepare(), timeout=timeout)
        response.raise_for_status()
        if not response.text:
            return {}
        result_json = response.json()
        logging.debug(
            (
                f"finish a request to API server, time elapsed: {time.time()-start_time:.3f}s, method: {method}, url:{url}"
                f", method: {method}, body: {body}, response body: {result_json}"
            )
        )
        return result_json
    except Exception as e:
        logging.warning(
            (
                f"failed to request API server, time elapsed: {time.time()-start_time:.3f}s, method: {method}, url:{url}, "
                f"error: {e.__class__.__name__} {e} {response.text if response else ''}"
            )
        )
        raise e


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workspace-id",
        dest="workspace_id",
        type=str,
        required=True,
        help="Set the workspace id.",
    )
    parser.add_argument(
        "--wav-path",
        dest="wav_path",
        type=str,
        required=True,
        help="Set the wav path.",
    )
    parser.add_argument(
        "--wav-name",
        dest="wav_name",
        type=str,
        required=True,
        help="Set the wav name.",
    )
    parser.add_argument(
        "--access-token",
        dest="access_token",
        type=str,
        required=True,
        help="The user's access token for the seameet api.",
    )
    parser.add_argument(
        "--meeting-name",
        dest="meeting_name",
        type=str,
        required=False,
        default="test meeting",
        help="Set the meeting name.",
    )
    parser.add_argument(
        "--meeting-language",
        dest="meeting_language",
        type=str,
        required=False,
        default="zh-TW",
        help="Set the meeting language.",
    )
    parser.add_argument(
        "--meeting-start-time",
        dest="meeting_start_time",
        type=str,
        required=False,
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        help="Set the meeting start time in the format of 'yyyy-mm-dd hh:mm:ss', UTC+0.",
    )
    parser.add_argument(
        "--seameet-url-base",
        dest="seameet_url_base",
        type=str,
        required=False,
        default="https://meet.seasalt.ai/seameet-api",
        help="the seameet url",
    )
    parser.add_argument(
        "--audio-start-offset",
        dest="audio_start_offset",
        type=int,
        required=False,
        default=0,
        help="indicate the audio start offset in seconds, relative to the start of the meeting.",
    )
    parser.add_argument(
        "--audio-format",
        dest="audio_format",
        type=str,
        required=False,
        default="wav",
        help="Set the audio format.",
    )
    parser.add_argument(
        "--audio-sample-rate",
        dest="audio_sample_rate",
        type=int,
        required=False,
        default=8000,
        help="Set the audio sample rate.",
    )
    parser.add_argument(
        "--audio-encoding",
        dest="audio_encoding",
        type=str,
        required=False,
        default="pcm_s8le",
        help="Set the audio encoding.",
    )
    parser.add_argument(
        "--scenario",
        dest="scenario",
        type=str,
        required=False,
        default="customer_service_call",
        help="Set the meeting scenario.",
    )
    parser.add_argument(
        "--customer-number",
        dest="customer_number",
        type=str,
        required=False,
        default="+886123456789",
        help="Set the customer number for the scenario: customer_service_call.",
    )
    parser.add_argument(
        "--customer-name",
        dest="customer_name",
        type=str,
        required=False,
        default="test customer",
        help="Set the customer name for the scenario: customer_service_call.",
    )
    parser.add_argument(
        "--agent-name",
        dest="agent_name",
        type=str,
        required=False,
        default="test agent",
        help="Set the agent name for the scenario: customer_service_call.",
    )
    parser.add_argument(
        "--direction",
        dest="direction",
        type=str,
        required=False,
        help="Set the meeting direction, INBOUND or OUTBOUND.",
    )
    parser.add_argument(
        "--enable-agent-recognition",
        dest="enable_agent_recognition",
        type=bool,
        required=False,
        default=True,
        help="enable_agent_recognition",
    )
    parser.add_argument(
        "--use-existing-audio",
        dest="use_existing_audio",
        type=bool,
        required=False,
        default=False,
        help="Use the meeting audio(all.wav) that already saved in seameet api.",
    )
    parser.add_argument(
        "--reset_meeting",
        dest="reset_meeting",
        type=bool,
        required=False,
        default=False,
        help="If it's true, it will delete all transcriptions and nlp things in the meeting before analyzing.",
    )
    parser.add_argument(
        "--queue_type",
        dest="queue_type",
        type=str,
        required=False,
        default="DEDICATED",
        help="The queue type=DEDICATED.",
    )

    args = parser.parse_args()
    main(args)

