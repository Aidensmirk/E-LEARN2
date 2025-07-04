import React, { useEffect, useState } from 'react';
import api from '../services/api';
import LessonDetail from './LessonDetail';

const LessonList = ({ moduleId }) => {
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedLesson, setSelectedLesson] = useState(null);

  useEffect(() => {
    const fetchLessons = async () => {
      try {
        const res = await api.get(`/api/modules/${moduleId}/lessons/`);
        setLessons(res.data);
      } catch (e) {
        setLessons([]);
      } finally {
        setLoading(false);
      }
    };
    fetchLessons();
  }, [moduleId]);

  if (loading) return <div>Loading lessons...</div>;
  if (!lessons.length) return <div>No lessons found.</div>;

  return (
    <div className="mb-4">
      <h3 className="text-lg font-semibold mb-1">Lessons</h3>
      <ul className="space-y-2">
        {lessons.map((lesson) => (
          <li key={lesson.id} className="bg-yellow-50 rounded p-2 cursor-pointer" onClick={() => setSelectedLesson(lesson)}>
            <div className="font-bold">{lesson.title}</div>
            <div className="text-gray-600">{lesson.content.slice(0, 100)}...</div>
            {lesson.video_url && (
              <span>
                {lesson.video_url.includes('youtube.com') || lesson.video_url.includes('youtu.be') || lesson.video_url.includes('vimeo.com') ? (
                  <iframe
                    src={lesson.video_url}
                    title="Lesson Video"
                    className="w-full h-48 my-2"
                    frameBorder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                  ></iframe>
                ) : (
                  <video src={lesson.video_url} controls className="w-full h-48 my-2" />
                )}
              </span>
            )}
            {lesson.file_attachment && (
              <video src={lesson.file_attachment} controls className="w-full h-48 my-2" />
            )}
          </li>
        ))}
      </ul>
      {selectedLesson && (
        <div className="mt-4 p-4 bg-white rounded shadow">
          <button className="mb-2 text-purple-600 underline" onClick={() => setSelectedLesson(null)}>
            &larr; Back to Lessons
          </button>
          <LessonDetail lesson={selectedLesson} courseId={lessons[0]?.module?.course || null} />
        </div>
      )}
    </div>
  );
};

export default LessonList;
