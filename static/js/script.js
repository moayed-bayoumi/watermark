const watermarkType = document.getElementById('watermark_type');
const watermarkText = document.getElementById('watermark_text');
const watermarkImage = document.getElementById('watermark_image');

watermarkType.addEventListener('change', () => {
  if (watermarkType.value === 'none') {
    watermarkText.style.display = 'none';
    watermarkImage.style.display = 'none';
  } else if (watermarkType.value === 'text') {
    watermarkText.style.display = 'block';
    watermarkImage.style.display = 'none';
  } else if (watermarkType.value === 'image') {
    watermarkText.style.display = 'none';
    watermarkImage.style.display = 'block';
  }
});
