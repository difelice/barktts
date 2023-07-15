# Bark TTS

Bark TTS is a Text-To-Speech component for [Home Assistant](https://home-assistant.io) that allows you to generate audio using AI-generated voices supported by Bark. It provides language support and the ability to choose different announcer speakers.

## Requirements

### Running Bark API

To use Bark TTS, you need to run the Bark API either in a self-hosted environment or through a cloud-based solution. Here are the steps to set it up:

#### Self-Hosted

##### Option 1: NVIDIA GPU

If you have an NVIDIA GPU, run the following command:

```shell
docker run --gpus=all --name=suno-ai-bark -p 5000:5000 --restart=unless-stopped --detach=true r8.im/suno-ai/bark@sha256:b76242b40d67c76ab6742e987628a2a9ac019e11d56ab96c4e91ce03b79b2787
```

##### Option 2: CPU Only (Slower)

If you don't have an NVIDIA GPU, use the following command:

```shell
docker run --name=suno-ai-bark --env=SUNO_USE_SMALL_MODELS=True -p 5000:5000 --restart=unless-stopped --detach=true r8.im/suno-ai/bark@sha256:b76242b40d67c76ab6742e987628a2a9ac019e11d56ab96c4e91ce03b79b2787
```

#### Cloud-Based

Cloud-based deployment options are still in development and coming soon.

> The Docker image is authored by [Replicate](https://replicate.com/).

## Installation

### Install the Custom Component

To install the custom component, you can use HACS (Home Assistant Community Store). Follow the steps below:

1. Go to the **HACS** panel.
2. Select **Integrations**.
3. On the top right corner, click the three dots menu and choose **Custom Repositories**.
4. Copy the URL `https://github.com/difelice/barktts` and paste it into the **Repository** field.
5. Select **Integration** as the category.

### Configure the Component

Add the following configuration to your `configuration.yaml` file:

- `url`: The URL of the Bark API server, including the `/predictions` endpoint.
- `lang`: The language for TTS. Optional. Defaults to the speaker `announcer`.

#### Example

> Replace `192.168.1.100` with the IP address of your Bark API Docker service mentioned above.

```yaml
tts:
  - platform: barktts
    url: http://192.168.1.100:5200/predictions
    lang: en
```
