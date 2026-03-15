from datetime import datetime

# SESSDATA 的过期时间戳
expires = 1777643550

expire_time = datetime.fromtimestamp(expires)
now = datetime.now()

print(f"SESSDATA 过期时间: {expire_time}")
print(f"当前时间: {now}")
print(f"剩余天数: {(expire_time - now).days} 天")

if expire_time > now:
    print("✅ 凭证未过期")
else:
    print("❌ 凭证已过期")
