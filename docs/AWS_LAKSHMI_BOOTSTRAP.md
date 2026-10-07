# Lakshmi AWS Bootstrap — Founder Action

Status checked: 2026-10-06 PT.

## Existing state

- IAM user exists: `aws-hackathon-s04-lakshmi`.
- Attached customer-managed policy: `S04-WBR-Lakshmi-LeastPrivilege`.
- IAM Identity Center is not enabled in this AWS account.
- No IAM console login profile currently exists for this user.
- No access key or other credential was created by the S04 engineering workflow.
- No account alias is configured; the AWS account-ID sign-in form would be required if IAM-user console access is enabled.

## Current least-privilege scope

The attached policy is restricted to S04 resources:
- S3: list/read/write on the S04 source and Athena-results buckets.
- Athena: query operations only in workgroup `S04-WBR`.
- Glue: catalog/database/table operations scoped to `s04_wbr`.
- Bedrock: invoke access for the approved Nova Micro model/inference-profile path.

It does not grant billing, IAM administration, or broad account administration.

## Founder bootstrap action

Franklyn must complete the authentication bootstrap personally in AWS.

Do not place any password, access key, MFA code, verification code, session token, or secret in GitHub, Slack, email, or ChatGPT.

If using IAM-user console access:
1. Open the AWS IAM console as the account administrator.
2. Select `aws-hackathon-s04-lakshmi`.
3. Enable console access / create the login profile using a temporary password.
4. Require password reset on first sign-in.
5. Deliver the temporary credential through an approved secure out-of-band channel.
6. Do not create a long-lived access key unless the team later proves CLI access is actually required.

Important: a forced first-login password reset requires the user to have permission to change their own password. The currently attached S04 policy does not include that permission. Adding such a permission is an access change and has intentionally NOT been made here.

## Required acceptance evidence

Do not claim Lakshmi's AWS access works until Lakshmi signs in under her own identity and returns service-level evidence:

- S3: pass/fail for the authorized S04 bucket path.
- Athena: pass/fail in workgroup `S04-WBR`.
- Glue: pass/fail for database `s04_wbr`.
- Bedrock: pass/fail for the approved invoke path.
- Exact non-sensitive error text for any failure.

Repo/GitHub access and IAM policy attachment are not service-level proof.

## Gate

No permission expansion, console password creation, access key creation, MFA change, or credential transmission is authorized by this document. Those remain founder actions / approval gates.
