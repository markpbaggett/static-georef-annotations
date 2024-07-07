% rebase('base.tpl')
% title = 'Static Georeferencing Annotations'
<div class="container mx-auto">
    <div style="padding-bottom: 20px;">
        <button class="btn btn-secondary" onclick="my_modal_1.showModal()">Get Image Regions</button>
    </div>
    <dialog id="my_modal_1" class="modal">
      <div class="modal-box" style="max-width: 800px;">
        <iframe src="/cropper" width="750" height="500"></iframe>
        <div class="modal-action">
          <form method="dialog">
            <button class="btn btn-secondary">Close</button>
          </form>
        </div>
      </div>
    </dialog>
    <div style="padding-bottom: 20px;">
        <button class="btn btn-secondary" onclick="my_modal_2.showModal()">Get Lat / Long</button>
    </div>
    <dialog id="my_modal_2" class="modal">
      <div class="modal-box" style="max-width: 800px;">
        <iframe src="/map" width="750" height="500"></iframe>
        <div class="modal-action">
          <form method="dialog">
            <button class="btn btn-secondary">Close</button>
          </form>
        </div>
      </div>
    </dialog>
</div>
