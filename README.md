# GPUmonitorbot

GPUmonitorbot can send GPU STATE information to a slack channel which is available webhook option.

## Purpose

The purpose of this bot is to monitor running GPUs for a calculation like Machine Learning. This bot can send information about current GPU state. If a calculation stopped, you can immediately realize that where ever you are on a slack channel.

## Requirement

This bot only supports NVIDIA GPU. Your emvironment needs to be able to do command `nvidia-smi`.

## Setting

Please make a `.env` file under the root directory like as the `envexample` file. You can get *WEBHOOK URL* of your slack channel  at [slack webhook](https://gpumonitor.slack.com/apps). 

## Usage

Move root directory, command `python GPUmonitor.py` at prompt.

## Options

| Option | Description |
| ----------- | ----------- |
| `--interval` | You can set interval time (minute). Default is 10 minutes. |