# Hugging Face Space Deploy Karne Ka Guide

## Step 1: HF Space Repository Clone Karo

```bash
# Terminal/PowerShell me ye command run karo
git clone https://huggingface.co/spaces/ubaid-ai/bot
cd bot
```

## Step 2: Files Copy Karo

Ab aapke local project se files copy karni hain. PowerShell me ye commands run karo:

```powershell
# D:\ai-chat-bot se bot folder me copy karo
Copy-Item "D:\ai-chat-bot\app_hf.py" -Destination . -Force
Copy-Item "D:\ai-chat-bot\requirements_hf.txt" -Destination . -Force
Copy-Item "D:\ai-chat-bot\Dockerfile" -Destination . -Force
Copy-Item "D:\ai-chat-bot\space.yaml" -Destination . -Force
Copy-Item "D:\ai-chat-bot\backend" -Destination . -Recurse -Force
```

Ya manually:
- `app_hf.py`
- `requirements_hf.txt`
- `Dockerfile`
- `space.yaml`
- `backend/` (puri folder)

## Step 3: Git Commit aur Push

```bash
git add .
git commit -m "Deploy AI Chat Bot backend"
git push
```

## Step 4: Environment Variables Set Karo

1. https://huggingface.co/spaces/ubaid-ai/bot par jao
2. **Settings** tab click karo
3. **Variables and secrets** section me jao
4. Ye secrets add karo (New secret click karke):

   - `JWT_SECRET_KEY` = `your-super-secret-jwt-key-at-least-32-characters-long`
   - `OPENAI_API_KEY` = `sk-your-openai-key` (agar chahiye)
   - `BETTER_AUTH_SECRET` = `your-better-auth-secret-at-least-32-characters`
   - `CSRF_SECRET_KEY` = `your-csrf-secret-key-at-least-32-characters`

**Note**: Agar ye variables set nahi kare, to app fallback values use karegi (demo mode).

## Step 5: Build Wait Karo

HF automatically build karega. **Logs** tab me check karo ki sab theek hai.

## Step 6: Test Karo

Browser me ye URLs open karo:

```
https://ubaid-ai-bot.hf.space/
https://ubaid-ai-bot.hf.space/health
```

Agar JSON response aaye, to backend deploy ho gaya hai! 🎉
