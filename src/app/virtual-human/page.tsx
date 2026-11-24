'use client';

import { useState } from 'react';
import HumanScene from '@/components/virtual-human/HumanScene';
import styles from './page.module.css';

interface ChatResponse {
      status: string;
      character_name: string;
      reply: string;
      emotion: Record<string, unknown>;
      relationship: Record<string, unknown>;
}

export default function VirtualHumanPage() {
      const [message, setMessage] = useState('');
      const [reply, setReply] = useState('');
      const [loading, setLoading] = useState(false);

      const sendMessage = async () => {
            if (!message.trim() || loading) {
                  return;
            }

            setLoading(true);

            try {
                  const response = await fetch('/api/ai/chat', {
                        method: 'POST',
                        headers: {
                              'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                              message: message,
                        }),
                  });

                  if (!response.ok) {
                        throw new Error('AI 서버 응답에 실패했습니다.');
                  }

                  const data: ChatResponse = await response.json();

                  setReply(data.reply);
                  setMessage('');

            } catch (error) {
                  console.error('AI Chat Error:', error);
                  setReply('AI 서버와 통신할 수 없습니다.');

            } finally {
                  setLoading(false);
            }
      };

      return (
            <main className={styles.container}>
                  <h1 className={styles.title}>
                        AI Virtual Human
                  </h1>

                  <section className={styles.scene}>
                        <HumanScene />
                  </section>

                  <section className={styles.chat}>
                        <div className={styles.reply}>
                              {reply || '캐릭터와 대화를 시작해 보세요.'}
                        </div>

                        <div className={styles.inputArea}>
                              <input
                                    type="text"
                                    value={message}
                                    onChange={(e) => setMessage(e.target.value)}
                                    onKeyDown={(e) => {
                                          if (e.key === 'Enter') {
                                                sendMessage();
                                          }
                                    }}
                                    placeholder="메시지를 입력하세요."
                                    disabled={loading}
                              />

                              <button
                                    onClick={sendMessage}
                                    disabled={loading || !message.trim()}
                              >
                                    {loading ? '응답 중...' : '전송'}
                              </button>
                        </div>
                  </section>
            </main>
      );
}