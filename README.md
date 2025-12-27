# AXION AI — Live Agentic AI System Using Pathway

## Overview
AXION AI is a prototype **agentic AI system** designed to reason over **live, continuously changing data** rather than static knowledge bases.

The project demonstrates how **Pathway’s streaming engine** can be used to build AI systems that avoid stale knowledge and adapt instantly to new inputs. AXION AI is being developed as part of the **Synaptix Frontier AI Hack @ IIT Madras**.

---

## Problem
Most AI systems today rely on static pipelines such as pre-indexed documents or batch-based RAG systems.  
Once indexed, their knowledge quickly becomes outdated, which is risky in real-world domains like healthcare, research, and compliance where information changes frequently.

---

## Solution
AXION AI is an **agentic AI system** that:
- Continuously ingests **live data streams**
- Updates its internal state in real time using **Pathway**
- Reasons over the latest information using an **agent-based architecture**
- Generates adaptive, context-aware outputs using an LLM

Unlike traditional systems, AXION AI does **not require re-indexing or restarting** when new data arrives.

---

## Architecture
![Architecture](architecture.png)

**High-level flow:**

Live Data → Pathway Streaming Engine → Agent Reasoning Layer → LLM → Output

Pathway enables real-time ingestion and incremental updates, while the agent layer handles multi-step reasoning.

---

## Hardware Prototype (Demo Source)
AXION AI includes an **early hardware prototype** that acts as a real-world data source for the system.

The prototype:
- Generates live sensor data
- Serves as a physical interface for demonstrating real-time AI reasoning
- Is used for system integration and feasibility demonstration

> ⚠️ Note: The hardware shown is a prototype and not a finalized or certified medical device.

![Hardware Demo](screenshots/IMG-20251224-WA0002.jpeg)

---

## Demo
The demo illustrates:
- Live data updates being introduced into the system
- Immediate changes in AI responses
- No system restart or re-indexing required

This highlights AXION AI’s ability to avoid stale knowledge and behave as a true agentic system.

---

## Setup Instructions

```bash
git clone https://github.com/yourusername/axion-ai
cd axion-ai
pip install -r requirements.txt
python src/demo.py
