from django.db import models


class Question(models.Model):
    id = models.AutoField(primary_key=True)  # Question ID
    subject_code = models.CharField(max_length=20)
    question_text = models.TextField()
    bloom_keyword = models.CharField(max_length=50, blank=True, null=True)  # Bloom Keyword
    bloom_level = models.CharField(max_length=2, blank=True, null=True)  # Bloom Level (e.g., C1, C2)

    def __str__(self):
        return f"{self.id} - {self.subject_code} - {self.bloom_keyword} (Level {self.bloom_level})"