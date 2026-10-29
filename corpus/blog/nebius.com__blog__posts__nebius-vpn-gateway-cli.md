# Nebius VPN Gateway CLI: Easily manage site-to-site VPNs in AI Cloud

Source: https://nebius.com/blog/posts/nebius-vpn-gateway-cli

Skip to main content

Teams running AI workloads often need private connectivity between the Nebius AI Cloud VPC and an external network, such as on-premises infrastructure, another cloud VPC or a partner environment. A site-to-site VPN provides an encrypted path over the public internet and it keeps private IP traffic off public endpoints. The challenge is making the gateway configuration repeatable, auditable and easy to operate when tunnels, routes and peers change.

The Nebius VPN Gateway CLI is an open source command line tool built by Nebius to create, configure and manage an IPsec VPN gateway inside the Nebius AI Cloud customer environment.

It is designed for technical teams, such as platform and network engineers, SREs, who want configuration as code, safe defaults and operational commands for validation and failover.

## Features and use casesFeatures and use cases

The Nebius VPN Gateway CLI provides IPsec connectivity using IKEv2 by default, with IKEv1 fallback when required. It uses pre-shared key authentication and modern cryptographic defaults such as AES-256 and SHA-256/384/512.

These capabilities enable teams to securely connect Nebius training and inference environment subnets to any on-premises infrastructure (e.g. Cisco IOS), partner environments, or other cloud VPCs (via GCP HA, AWS Site to Site VPN, Azure VPN Gateway), without exposing private services to the public internet.

The gateway supports both BGP and static routing, making it suitable for enterprise network extensions as well as simpler peer setups that require explicit route control. High availability is supported through multi-tunnel configurations with automatic or manual failover, which is especially useful for production AI platforms that require predictable connectivity.

## How it worksHow it works

The VPN gateway is deployed inside your Nebius AI Cloud VPC environment and uses a dedicated subnet in your VPC named vpngw-subnet.

In simple terms:

- You create a subnet called vpngw-subnet in the target VPC;

- The CLI provisions a gateway group, implemented as one or more VM instances attached to the vpngw-subnet;

- The gateway establishes IPsec tunnels to your peer gateway using parameters from your YAML configuration;

- Routing is configured as either BGP or static, based on your preference and what the peer supports;

- The CLI can also program local routes so your application subnets forward traffic to the VPN gateway.

This model keeps all VPN data plane components inside your VPC, while the CLI provides a consistent, repeatable control plane workflow.

### Routing options: BGP or staticRouting options: BGP or static

BGP is a good default for production because it reduces manual route management as networks grow, and it helps converge after changes. Static routing is useful when the peer does not support BGP, or when you prefer explicit route control.

Set routing mode in the YAML configuration:

routing: 
 mode: "bgp" # bgp|static 

## Getting startedGetting started

Install the CLI

The CLI is published as a Python wheel in the Nebius professional services releases.

- Releases page, use it to download the latest version

Example install for version v0.4.9:

wget https://github.com/nebius/nebius-ps-services/releases/download/nebius-vpngw-v0.4.9/nebius_vpngw-0.4.9-py3-none-any.whl 

pipx install ./nebius_vpngw-0.4.9-py3-none-any.whl 

Verify installation:

nebius-vpngw --version 
nebius-vpngw --help 

Generate the YAML configuration

nebius-vpngw create-config my-vpn.config.yaml

What you need from the peer gateway first

Before you apply, you will need these values from the peer gateway side:

- 

Remote ASN number: example 65014

- 

Number of tunnels: example 2

- 

For each tunnel:

- Remote public IP address

- Pre shared key (PSK)

- Inner tunnel CIDR, example 169.254.5.152/30

- Inner local IP, example 169.254.5.154

- Inner remote IP, example 169.254.5.153

## Apply, create route and validateApply, create route and validate

Apply the configuration:

nebius-vpngw apply --local-config-file my-vpn.config.yaml 

Add local routes:

nebius-vpngw add-routes-local --local-config-file my-vpn.config.yaml 

Verify routes:

nebius-vpngw list-routes-local --local-config-file my-vpn.config.yaml

Check gateway and tunnel status:

nebius-vpngw status --local-config-file my-vpn.config.yaml

## High availability and failoverHigh availability and failover

Active and passive HA for multi tunnel connections

For multi tunnel connections, the gateway operates in active and passive mode, one tunnel carries traffic, the other remains ready to take over.

Example configuration:

connections: 
 - name: "gcp-ha-vpn" 
 routing_mode: bgp 
 tunnels: 
 - name: "tunnel-1" 
 ha_role: "active" # Primary, carries traffic 
 # ... 
 - name: "tunnel-2" 
 ha_role: "passive" # Standby, automatic failover 
 # ... 

Manual failover and failback

In addition to automatic failover in case of any failure, the CLI provides explicit commands to switch traffic to a standby tunnel and then revert back when you are ready. This is useful for planned maintenance, peer changes, or operational testing.

Failover example:

nebius-vpngw failover --tunnel-failover tunnel-2 --local-config-file <file>

Failback example:

nebius-vpngw failback --tunnel-failback tunnel-1 --local-config-file <file>

## Why it matters for teams building on NebiusWhy it matters for teams building on Nebius

Nebius AI Cloud is optimized for demanding AI workloads in products that depend on reliable network connectivity to data, services and operational tooling. Nebius VPN Gateway CLI provides a practical path to private connectivity that is secure, repeatable and operator friendly, with clear validation and failover workflows. To learn more, check out our GitHub page.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Reza Bahmanzadeh
AI Engineer at Nebius

Contents

- 

Features and use cases

- 

How it works

- Routing options: BGP or static

- 

Getting started

- 

Apply, create route and validate

- 

High availability and failover

- 

Why it matters for teams building on Nebius

## See also

### 

Serving LLMs with vLLM: A practical inference guide

This guide teaches the essentials of serving large language models with vLLM. It builds from foundational neural network concepts, like transformers and attention, to introduce practical inference workflows, explore useful vLLM features and offer hands-on, operational guidance for efficient deployments.

December 18, 2025
14 mins to read

### 

Introducing NVIDIA RTX PRO 6000 Blackwell Server Edition on Nebius

NVIDIA RTX PRO 6000 Blackwell opens new opportunities for cost-efficient inference and increased performance for visual computing and scientific simulations.

March 26, 2026
5 mins to read

### 

Nebius AI Cloud “Aether 3.5”: Frictionless compute for real world AI

This release introduces new serverless capabilities, the NVIDIA RTX PRO™ 6000 Blackwell Server Edition GPU for applied AI use cases, improved cluster configuration tools, streamlined data operations and platform-level enhancements that reduce routine complexity while preserving full control.

March 26, 2026
8 mins to read

Sign in to save this post
Sign In
